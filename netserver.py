# -*- coding: utf-8 -*-
"""
May chu chia se benh_nhan.db cho nhieu may trong cung mang LAN noi bo
(khong dung Internet/cloud). Chi dung thu vien chuan (http.server) - khong
them dependency moi, de khong phai sua build.bat/setup.iss/requirements.txt.

Giao thuc: HTTP POST /rpc, body JSON {"op": ...}. Xem netclient.py o phia
may tram (client) - noi bat chuoc lai giao dien sqlite3.Connection/Cursor
toi thieu ma core.py can, de core.py + app.py khong phai sua logic doc/ghi.

Cac op bat dau bang "admin_" (xem quan ly ket noi/whitelist IP ben duoi)
chi duoc phep goi tu chinh may chu (localhost) - dung boi server_tray.py,
KHONG phai danh cho may tram goi qua mang.

CANH BAO BAO MAT: mac dinh KHONG yeu cau xac thuc (dung API key trong
core.get_lan_api_key() de bat, tuy chon) - bat ky may nao trong cung mang
LAN deu goi duoc RPC nay, bao gom ca cau lenh SQL tuy y ma tab "Truy vấn
SQL" tren may tram gui len (da duoc gioi han o phia may tram la chi
SELECT, nhung may chu khong tu kiem tra lai dieu do). Chi bat che do may
chu trong mang noi bo tin cay. Co the gioi han theo IP (whitelist) qua
menu tray "Quản lý IP được phép kết nối" - xem core.load_acl_config().
"""
import json
import socket
import sqlite3
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import core

SESSION_IDLE_TIMEOUT = 15 * 60  # giay - tu dong dong phien khong hoat dong
LOCALHOST_IPS = ("127.0.0.1", "::1")

_httpd = None
_httpd_thread = None
_reaper_thread = None
_reaper_stop = threading.Event()
_sessions = {}
_sessions_lock = threading.Lock()


def get_local_ip():
    """Doan dia chi IP LAN cua may nay (khong thuc su gui goi tin ra ngoai)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def _is_ip_allowed(ip):
    """Localhost (chinh may chu) luon duoc phep, de tray khong bao gio tu
    khoa minh. Cac IP khac chi bi gioi han khi che do "whitelist" duoc bat."""
    if ip in LOCALHOST_IPS:
        return True
    cfg = core.load_acl_config()
    if cfg.get("mode") != "whitelist":
        return True
    return ip in (cfg.get("allowed_ips") or [])


def _new_connection():
    conn = sqlite3.connect(core.DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def _reap_idle_sessions():
    while not _reaper_stop.is_set():
        if _reaper_stop.wait(60):
            return
        now = time.time()
        with _sessions_lock:
            stale = [sid for sid, s in _sessions.items()
                     if now - s["last_used"] > SESSION_IDLE_TIMEOUT]
            for sid in stale:
                try:
                    _sessions[sid]["conn"].close()
                except Exception:
                    pass
                del _sessions[sid]


def _row_to_list(row):
    return [row[k] for k in row.keys()]


class RpcHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass  # im lang, khong spam console cua ung dung

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/rpc":
            self._send_json(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", 0) or 0)
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            self._send_json(400, {"error": "JSON không hợp lệ"})
            return

        client_ip = self.client_address[0]
        op = payload.get("op")
        is_admin_op = isinstance(op, str) and op.startswith("admin_")
        if is_admin_op:
            if client_ip not in LOCALHOST_IPS:
                self._send_json(403, {"error": "Chỉ quản trị được từ chính máy chủ (localhost)"})
                return
        elif not _is_ip_allowed(client_ip):
            self._send_json(403, {"error": "Địa chỉ IP này không được phép kết nối tới máy chủ"})
            return

        api_key = core.get_lan_api_key()
        if api_key and self.headers.get("X-Api-Key") != api_key:
            self._send_json(401, {"error": "Sai hoặc thiếu khóa API"})
            return

        try:
            result = self._dispatch(payload)
            self._send_json(200, result)
        except KeyError as e:
            self._send_json(400, {"error": f"Thiếu tham số: {e}"})
        except sqlite3.Error as e:
            self._send_json(400, {"error": str(e)})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _dispatch(self, payload):
        op = payload.get("op")

        if op == "ping":
            return {"ok": True, "version": core.get_local_version()}

        if op == "backup":
            path = core.backup_database(payload.get("reason", "tu_xa"), payload.get("keep", 10))
            return {"path": path}

        if op == "admin_list_connections":
            now = time.time()
            with _sessions_lock:
                connections = [
                    {
                        "session_id": sid,
                        "ip": s["ip"],
                        "connected_at": s["connected_at"],
                        "idle_seconds": round(now - s["last_used"], 1),
                    }
                    for sid, s in _sessions.items()
                ]
            return {"connections": connections}

        if op == "admin_disconnect":
            sid = payload.get("session_id")
            ip = payload.get("ip")
            closed = 0
            with _sessions_lock:
                if sid:
                    targets = [sid] if sid in _sessions else []
                elif ip:
                    targets = [k for k, s in _sessions.items() if s["ip"] == ip]
                else:
                    targets = []
                for k in targets:
                    try:
                        _sessions[k]["conn"].close()
                    except Exception:
                        pass
                    del _sessions[k]
                    closed += 1
            return {"ok": True, "closed": closed}

        if op == "admin_get_acl":
            return core.load_acl_config()

        if op == "admin_set_acl":
            mode = payload.get("mode", "allow_all")
            if mode not in ("allow_all", "whitelist"):
                raise sqlite3.Error(f"Chế độ không hợp lệ: {mode}")
            allowed_ips = [str(ip).strip() for ip in (payload.get("allowed_ips") or []) if str(ip).strip()]
            core.save_acl_config({"mode": mode, "allowed_ips": allowed_ips})
            return {"ok": True}

        if op == "connect":
            sid = uuid.uuid4().hex
            now = time.time()
            with _sessions_lock:
                _sessions[sid] = {
                    "conn": _new_connection(),
                    "lock": threading.Lock(),
                    "last_used": now,
                    "connected_at": now,
                    "ip": self.client_address[0],
                }
            return {"session_id": sid}

        if op == "close":
            sid = payload["session_id"]
            with _sessions_lock:
                session = _sessions.pop(sid, None)
            if session is not None:
                try:
                    session["conn"].close()
                except Exception:
                    pass
            return {"ok": True}

        sid = payload["session_id"]
        with _sessions_lock:
            session = _sessions.get(sid)
        if session is None:
            raise sqlite3.Error("Phiên kết nối đã hết hạn, vui lòng thử lại.")

        with session["lock"]:
            session["last_used"] = time.time()
            conn = session["conn"]
            if op == "commit":
                conn.commit()
                return {"ok": True}
            if op == "execute":
                cur = conn.execute(payload["sql"], payload.get("params") or [])
                return self._cursor_result(cur)
            if op == "executemany":
                cur = conn.executemany(payload["sql"], payload.get("seq_params") or [])
                return {"columns": None, "rows": None, "rowcount": cur.rowcount, "lastrowid": cur.lastrowid}
            raise sqlite3.Error(f"Thao tác không hỗ trợ: {op}")

    def _cursor_result(self, cur):
        if cur.description is None:
            return {"columns": None, "rows": None, "rowcount": cur.rowcount, "lastrowid": cur.lastrowid}
        columns = [d[0] for d in cur.description]
        rows = [_row_to_list(r) for r in cur.fetchall()]
        return {"columns": columns, "rows": rows, "rowcount": cur.rowcount, "lastrowid": cur.lastrowid}


def is_running():
    return _httpd is not None


def start_server(port=8765):
    """Bat may chu chia se qua mang LAN (idempotent - goi lai khi da chay
    thi khong lam gi). Chay ngay trong tien trinh ung dung hien tai, o cac
    luong nen (thread) rieng - khong chan giao dien."""
    global _httpd, _httpd_thread, _reaper_thread
    if _httpd is not None:
        return
    core.init_db()
    _httpd = ThreadingHTTPServer(("0.0.0.0", port), RpcHandler)
    _httpd_thread = threading.Thread(target=_httpd.serve_forever, daemon=True)
    _httpd_thread.start()
    _reaper_stop.clear()
    _reaper_thread = threading.Thread(target=_reap_idle_sessions, daemon=True)
    _reaper_thread.start()


def stop_server():
    global _httpd, _httpd_thread, _reaper_thread
    if _httpd is None:
        return
    _httpd.shutdown()
    _httpd.server_close()
    _httpd = None
    _httpd_thread = None
    _reaper_stop.set()
    _reaper_thread = None
    with _sessions_lock:
        for session in _sessions.values():
            try:
                session["conn"].close()
            except Exception:
                pass
        _sessions.clear()
