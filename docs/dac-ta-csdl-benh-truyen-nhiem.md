# ĐẶC TẢ CƠ SỞ DỮ LIỆU GIÁM SÁT BỆNH TRUYỀN NHIỄM

**Phạm vi:** Chỉ mảng **giám sát bệnh truyền nhiễm** (Chương II Thông tư 15/2026/TT-BYT và Phụ lục I Quyết định 97/QĐ-PB). Các mảng bệnh không lây nhiễm, rối loạn tâm thần, dinh dưỡng, thương tích **đã được tách khỏi** phạm vi CSDL này.

**Căn cứ pháp lý (nghiệp vụ):**
- Thông tư số 15/2026/TT-BYT ngày 17/5/2026 của Bộ trưởng Bộ Y tế quy định chi tiết một số điều của Luật Phòng bệnh số 114/2025/QH15 (hiệu lực 01/7/2026) — Chương II.
- Quyết định số 97/QĐ-PB ngày 30/6/2026 của Cục trưởng Cục Phòng bệnh — Phụ lục I (danh mục bệnh truyền nhiễm báo cáo theo thời gian; Mẫu 01–05).

**Chuẩn mã hóa dữ liệu Việt Nam áp dụng** (chi tiết tại Phần J):
- **Thông tư 06/2026/TT-BYT** — mã hóa bệnh tật theo **ICD-10**.
- **Quyết định 19/2025/QĐ-TTg** — mã đơn vị hành chính (mô hình 2 cấp tỉnh/xã, hiệu lực 01/7/2025).
- **Quyết định 4210/QĐ-BYT** — bộ danh mục chuẩn ngành y tế (mã giới tính, dân tộc, quốc gia, nghề nghiệp).
- **Luật Căn cước 2023** + **Quyết định 2153/QĐ-BYT** — số định danh cá nhân (12 chữ số) và mã định danh y tế.
- **Quyết định 5937/QĐ-BYT** — mã cơ sở khám bệnh, chữa bệnh.

**Ghi chú về nguồn:** Mọi bảng/trường được ánh xạ tới Điều/Khoản TT15 hoặc Mẫu/Phụ lục I QĐ97 (ghi trong cột "Căn cứ"/dưới tên bảng). Phần đề xuất kỹ thuật thuần túy (bổ sung để vận hành hệ thống) được đánh dấu **[Đề xuất kỹ thuật]**.

---

## PHẦN A. TỔNG QUAN

### A.1. Mục tiêu
Theo Điều 3 TT15, Hệ thống thông tin giám sát trong phòng bệnh có chức năng tiếp nhận, cập nhật, quản lý, tổng hợp, phân tích, khai thác, phản hồi, chia sẻ dữ liệu về bệnh truyền nhiễm. CSDL này mô hình hóa phần **bệnh truyền nhiễm**: đối tượng giám sát, ca bệnh, ổ dịch, khai báo, đánh giá nguy cơ, cảnh báo, điều tra – xử lý ổ dịch, phân loại nhóm bệnh & xác định dịch, báo cáo dịch.

### A.2. Mô hình phân cấp đơn vị (Điều 10, 26)
```
Cấp xã     : Trạm Y tế cấp xã (TYT), Cơ sở khám bệnh chữa bệnh (CSKCB),
              Cơ sở xét nghiệm, Tổ chức kiểm dịch y tế tại cửa khẩu
Cấp tỉnh   : Cơ quan chuyên môn về y tế thuộc UBND tỉnh (Sở Y tế),
              Trung tâm Kiểm soát bệnh tật cấp tỉnh (TTKSBT/CDC), Trung tâm Kiểm dịch y tế quốc tế
Cấp vùng   : Viện VSDT Trung ương/Tây Nguyên, Viện Pasteur TP.HCM/Nha Trang,
              Viện Sốt rét – KST – Côn trùng TW/Quy Nhơn/TP.HCM
Trung ương : Cục Phòng bệnh (đầu mối quốc gia), Cục Quản lý Khám chữa bệnh,
              Bệnh viện Phổi Trung ương (đầu mối bệnh lao)
```
→ `dm_don_vi` mô hình hóa cây này qua `don_vi_cha_id` + `dm_loai_don_vi` + `dm_dia_ban_phu_trach`.

### A.3. Ba loại hình giám sát (Điều 6)
| Loại hình | Điều | Mô tả |
|---|---|---|
| Giám sát dựa vào chỉ số | 6.1, 7 | Thu thập thường xuyên, liên tục, toàn quốc |
| Giám sát trọng điểm | 6.2, 8 | Thu thập chuyên sâu tại điểm giám sát được chọn |
| Giám sát dựa vào sự kiện | 6.3, 9 | Sàng lọc/xác minh tín hiệu từ cộng đồng, mạng xã hội, CSKCB, ngành NN&MT |
→ Ghi nhận qua `dm_loai_hinh_giam_sat` (thuộc tính trên bản ghi nghiệp vụ).

### A.4. Nguyên tắc thiết kế
1. Tách dữ liệu vi mô (ca bệnh, ổ dịch) khỏi dữ liệu tổng hợp (báo cáo tình hình dịch) — dùng `dm_chi_tieu` + `bc_chi_tieu_thong_ke`. **[Đề xuất kỹ thuật]**
2. Danh mục dùng chung tập trung: mã bệnh/ICD-10 lấy từ Danh mục 01 PL I QĐ97, không hard-code.
3. Truy vết đơn vị & luồng báo cáo: mọi bản ghi nghiệp vụ có `don_vi_id`.
4. An toàn dữ liệu cá nhân (Điều 3.3): kiểm soát truy cập, mã hóa, nhật ký (Phần H).
5. Định danh cá nhân dùng chung (`nguoi`) theo số định danh cá nhân/mã định danh y tế. **[Đề xuất kỹ thuật]**

---

## PHẦN B. QUY ƯỚC CHUNG
- Tiền tố: `dm_` danh mục dùng chung · `btn_` bệnh truyền nhiễm · `bc_` báo cáo/thống kê · `ht_` hệ thống.
- Khóa chính `id BIGINT` tự tăng; bảng nghiệp vụ có cột chuẩn: `don_vi_id, nguoi_tao_id, ngay_tao, nguoi_cap_nhat_id, ngay_cap_nhat, trang_thai`.
- Ký hiệu: **PK** khóa chính · **FK** khóa ngoại · **NN** NOT NULL · **UQ** duy nhất.

---

## PHẦN C. DANH MỤC DÙNG CHUNG

### C.1. `dm_dia_ban_hanh_chinh` — Đơn vị hành chính (tỉnh/xã)
| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| ma_dia_ban | VARCHAR(10) | UQ, NN | Tỉnh 2 chữ số (01–99); xã 5 chữ số (00001–99999) |
| ten_dia_ban | VARCHAR(200) | NN | Tên xã/phường/đặc khu hoặc tỉnh/thành phố |
| cap | VARCHAR(10) | NN | `xa` \| `tinh` (2 cấp, không còn cấp huyện) |
| dia_ban_cha_id | BIGINT | FK→ chính bảng | Tỉnh cha (nếu cấp = xã) |

> **CHUẨN MÃ:** Quyết định 19/2025/QĐ-TTg (hiệu lực 01/7/2025; 34 tỉnh, 3.321 xã; Cục Thống kê – Bộ Tài chính quản lý).

### C.2. `dm_loai_don_vi` — Loại hình đơn vị
Giá trị: `tram_y_te_xa`, `cskcb`, `cs_xet_nghiem`, `so_y_te`, `ttksbt_tinh`, `tt_kiem_dich_yt_quoc_te`, `vien_vsdt_pasteur`, `vien_sot_ret_kst_con_trung`, `benh_vien_tw`, `benh_vien_phoi_tw`, `cuc_phong_benh`, `cuc_ql_kham_chua_benh`, `to_chuc_kiem_dich_yt_cua_khau`. *(Điều 10 TT15)*

### C.3. `dm_don_vi` — Đơn vị/cơ sở y tế
| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| ma_don_vi | VARCHAR(20) | UQ, NN | Mã cơ sở KCB do Bộ Y tế cấp (**QĐ 5937/QĐ-BYT**) |
| ten_don_vi | VARCHAR(300) | NN | |
| loai_don_vi_id | BIGINT | FK→dm_loai_don_vi | |
| dia_ban_id | BIGINT | FK→dm_dia_ban_hanh_chinh | |
| don_vi_cha_id | BIGINT | FK→ chính bảng | Đơn vị quản lý trực tiếp (cây báo cáo) |
| dia_chi, dien_thoai, email | VARCHAR | | |
| trang_thai_hoat_dong | BOOLEAN | NN | |

### C.4. `dm_dia_ban_phu_trach` — Phân công địa bàn phụ trách của các Viện
`id, vien_id FK, tinh_id FK, linh_vuc='benh_truyen_nhiem'` — *Điều 10.3 (6 Viện VSDT/Pasteur/SR-KST-CT phụ trách theo địa bàn Bộ Y tế phân công)*.

### C.5. `dm_benh_truyen_nhiem` — Danh mục bệnh truyền nhiễm
| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| ma_benh | VARCHAR(20) | UQ, NN | Mã nội bộ |
| ten_benh | VARCHAR(300) | NN | |
| nhom_phan_loai | CHAR(1) | CHECK IN ('A','B','C') | Theo Điều 15 (tính theo điểm — quy tắc G.1) |
| ky_han_bao_cao | VARCHAR(20) | NN | `24h` \| `48h` \| `tuan` (Danh mục 01 PL I QĐ97) |
| diem_muc_do_nghiem_trong | TINYINT | CHECK 1..3 | Tiêu chí 1 (Phụ lục I TT15) |
| diem_kha_nang_lay_lan | TINYINT | CHECK 1..3 | Tiêu chí 2 |
| diem_can_thiep_vacxin_thuoc | TINYINT | CHECK 1..3 | Tiêu chí 3 |
| diem_muc_do_luu_hanh_tiem_nang_dich | TINYINT | CHECK 1..3 | Tiêu chí 4 |
| tong_diem | TINYINT | tính toán (4–12) | A ≥10 (hoặc ĐBNH mới phát sinh chưa rõ tác nhân); B 7–9; C <7 |
| luu_hanh_tai_dia_phuong | BOOLEAN | | Dùng cho quy tắc xác định dịch (Điều 16.1.b/c) |
| ghi_chu | TEXT | | |

**Dữ liệu nạp sẵn:** 81 bệnh (18 báo cáo 24h, 17 báo cáo 48h, 46 báo cáo tuần) — xem `danh-muc-benh-truyen-nhiem.md`, `du-lieu-mau-benh-truyen-nhiem.csv`, `seed_dm_benh_truyen_nhiem.sql`.

### C.6. `dm_benh_truyen_nhiem_icd10` — Mã ICD-10 của bệnh
`id, benh_id FK, ma_icd10 VARCHAR(10)` — một bệnh có thể có nhiều mã ICD-10 (vd A80, A20, J09...). **CHUẨN: TT 06/2026/TT-BYT.** Bệnh chưa có mã ICD-10 vẫn báo cáo trực tiếp (ghi chú Danh mục 01).

### C.7. Danh mục nhỏ khác
- `dm_nghe_nghiep`: nghề nghiệp đối tượng giám sát (trường Nghề nghiệp ở Mẫu 01 PL I). **CHUẨN: QĐ 4210/QĐ-BYT (bảng NGHENGHIEP).**
- `dm_dan_toc`: mã 2 chữ số, 54 dân tộc. **CHUẨN: QĐ 4210/QĐ-BYT (bảng DANTOC).**
- `dm_muc_do_nguy_co_dot_xuat`: Thấp / Trung bình / Cao / Rất cao *(Điều 21.2)*.
- `dm_cap_do_phong_thu_dan_su`: Cấp 1 / 2 / 3 / Tình trạng khẩn cấp *(Điều 17–20)*.
- `dm_loai_hinh_giam_sat`: Dựa vào chỉ số / Trọng điểm / Dựa vào sự kiện *(Điều 6)*.
- `dm_ky_bao_cao`: Ngày / Tuần / Tháng / Đột xuất.

### C.8. `nguoi` — Hồ sơ cá nhân dùng chung *[Đề xuất kỹ thuật]*
| Trường | Kiểu | Ràng buộc | Mô tả / CHUẨN |
|---|---|---|---|
| id | BIGINT | PK | |
| ho_ten | VARCHAR(200) | NN | Mẫu 01 PL I |
| so_dinh_danh_ca_nhan | VARCHAR(12) | UQ | 12 chữ số — **Luật Căn cước 2023** |
| ma_dinh_danh_y_te | VARCHAR(20) | UQ | = số định danh cá nhân — **QĐ 2153/QĐ-BYT** |
| ngay_sinh | DATE | | Có thể chỉ có năm sinh |
| gioi_tinh | CHAR(1) | CHECK IN('1','2','3') | **1=Nam, 2=Nữ, 3=Chưa xác định — QĐ 4210/QĐ-BYT** |
| dan_toc_id | BIGINT | FK→dm_dan_toc | Mã dân tộc (QĐ 4210) |
| quoc_tich | CHAR(3) | | ISO 3166-1 alpha-3 / QĐ 4210 (vd VNM) |
| nghe_nghiep_id | BIGINT | FK→dm_nghe_nghiep | |
| dien_thoai | VARCHAR(20) | | DLCN |
| dia_chi_hien_tai | VARCHAR(500) | | Số nhà, đường/tổ/thôn, phường/xã, tỉnh |
| dia_chi_thuong_tru | VARCHAR(500) | | |
| dia_ban_id | BIGINT | FK→dm_dia_ban_hanh_chinh | Xã quản lý (mã theo QĐ 19/2025) |
| noi_lam_viec_hoc_tap | VARCHAR(300) | | Điều 7.1a |

---

## PHẦN D. BẢNG NGHIỆP VỤ BỆNH TRUYỀN NHIỄM (`btn_*`)

### D.1. `btn_doi_tuong_giam_sat` — Đối tượng giám sát *(Điều 5, 7.1a)*
`id, nguoi_id FK, loai_doi_tuong [mac_benh|mang_mam_benh|nghi_ngo|tiep_xuc|tu_vong_do_hoac_nghi_ngo], don_vi_phat_hien_id FK, ngay_phat_hien DATETIME`

### D.2. `btn_truong_hop_benh` — Báo cáo trường hợp bệnh *(Mẫu 01 PL I; Điều 10.2a)*
| Trường | Kiểu | Mô tả |
|---|---|---|
| id | BIGINT PK | |
| doi_tuong_giam_sat_id | FK | |
| benh_id | FK→dm_benh_truyen_nhiem | |
| phan_loai_bao_cao | `24h`\|`48h`\|`tuan` | |
| tinh_trang_tiem_chung | `co`\|`khong`\|`khong_ro` | DLCN |
| so_lan_tiem | INT | nếu tiêm chủng = có |
| phan_loai_chan_doan | `lam_sang_nghi_ngo`\|`xac_dinh_ptn` | |
| ngay_khoi_phat | DATE | |
| da_lay_mau_xn | BOOLEAN | |
| loai_xet_nghiem | `test_nhanh`\|`huyet_thanh_hoc`\|`pcr_rtpcr`\|`khac` | |
| ket_qua_xet_nghiem | `duong_tinh`\|`am_tinh`\|`nghi_ngo`\|`chua_co_ket_qua` | |
| tinh_trang_dieu_tri | `ngoai_tru`\|`noi_tru` | |
| ngay_nhap_vien, ngay_ra_vien_chuyen_vien_tu_vong | DATE | |
| ket_qua_cuoi | `ra_vien`\|`chuyen_vien`\|`tu_vong`\|`khac` | |
| tien_su_dich_te | TEXT | Đi lại, tiếp xúc người bệnh/động vật, phơi nhiễm (DLCN) |
| nguoi_bao_cao_id | FK→ht_nguoi_dung | |
| don_vi_bao_cao_id | FK→dm_don_vi | TYT xã/CSKCB/cơ sở xét nghiệm |
| o_dich_id | FK→btn_o_dich | nếu ca thuộc 1 ổ dịch |

### D.3. `btn_o_dich` — Ổ dịch *(Điều 2.1; Mẫu 02, 03 PL I)*
`id, ten_o_dich, benh_id FK, don_vi_id FK (TYT xã), dia_diem (thôn/tổ, xã, tỉnh), ngay_khoi_phat_ca_dau, ngay_nhap_canh, ngay_den_dia_phuong, ngay_nhan_bao_cao_dau, ngay_khoi_phat_ca_cuoi, ngay_ket_thuc_hoat_dong, mo_ta_yeu_to_nguy_co, trang_thai [dang_hoat_dong|da_ket_thuc]`

- `btn_o_dich_so_lieu_ngay` *(Mẫu 02 mục 2,3)*: `id, o_dich_id FK, ngay, thon_to, so_mac, so_tu_vong, so_mau_lam_xn, so_xn_duong_tinh`
- `btn_o_dich_tong_hop` *(Mẫu 03 mục 7)*: `o_dich_id FK(PK), tong_so_mac, tong_so_tu_vong, tong_so_mau_xn, tong_so_mau_duong_tinh`

### D.4. `btn_bao_cao_dich_benh` — Thông tin/Báo cáo có dịch – hết dịch *(Điều 25, 26; Mẫu 01/02 PL II TT15)*
`id, o_dich_id FK, don_vi_id FK (TYT xã), loai_thong_tin [co_dich|het_dich], ten_dich_benh, thoi_gian_xac_dinh, thoi_gian_het_dich, dia_diem_o_dich, khuyen_nghi, so_van_ban, ngay_ban_hanh (≤24h kể từ khi xác định), nguoi_ky_id FK, noi_nhan`

- `btn_bao_cao_dich_benh_chi_tiet` *(Mẫu 04/05 PL I — cấu trúc I–VIII)*: các cột text theo đúng mục (đặc điểm tình hình; số mắc/tử vong so sánh; kết quả XN; phân tích thời gian–địa điểm–con người; yếu tố trung gian/véc tơ; bệnh trên động vật; biện pháp đã triển khai; huy động nguồn lực; đánh giá – nhận định – dự báo; khó khăn; giải pháp; đề xuất).

### D.5. `btn_khai_bao_ca_nhan` — Khai báo bệnh truyền nhiễm *(Điều 12, 13)*
`id, nguoi_id FK, cach_thuc_khai_bao [dien_thoai|truc_tiep|hinh_thuc_khac|ung_dung_dien_tu], don_vi_tiep_nhan_id FK (TYT/CSKCB/kiểm dịch cửa khẩu), tinh_trang_suc_khoe, tien_su_tiep_xuc_di_chuyen, ngay_khai_bao, ket_qua_xu_ly`

### D.6. `btn_danh_gia_nguy_co` — Đánh giá nguy cơ *(Điều 21)*
`id, loai_danh_gia [hang_nam|dot_xuat], benh_id FK, don_vi_id FK, ky_danh_gia (năm), ngay_danh_gia, dau_hieu_kich_hoat (8 dấu hiệu Điều 21.2 a–h), muc_do_nguy_co [thap|trung_binh|cao|rat_cao], yeu_to_gia_tang, nang_luc_nguon_luc, bien_phap_de_xuat`

### D.7. `btn_canh_bao_dich_benh` — Cảnh báo dịch *(Điều 22)*
`id, benh_id FK, don_vi_dia_ban_id FK (TYT xã), dieu_kien_kich_hoat [nhom_a_1_ca|nhom_bc_luu_hanh_vuot_nguong|nhom_bc_khong_luu_hanh_3ca|benh_moi_chua_ghi_nhan], ngay_canh_bao, noi_dung_nguy_co, bien_phap_phong_chong`

### D.8. `btn_cap_do_phong_thu_dan_su` — Cấp độ PTDS/khẩn cấp *(Điều 17–20)*
`id, cap_do [cap_1|cap_2|cap_3|khan_cap], dia_ban_id FK, benh_id FK, ngay_ban_bo, ngay_bai_bo, can_cu_tieu_chi`

### D.9. `btn_dieu_tra_o_dich` — Nhật ký điều tra 10 bước *(Điều 23)*
`id, o_dich_id FK, buoc [chuan_bi|xac_minh_chan_doan|khang_dinh_ton_tai|dieu_tra_phat_hien_truong_hop|mo_ta_3_yeu_to|xay_dung_gia_thuyet|danh_gia_kiem_dinh|hoan_thien_gia_thuyet|de_xuat_bien_phap|bao_cao_ket_qua], noi_dung, ngay_thuc_hien, nguoi_thuc_hien_id FK`

### D.10. `btn_bien_phap_xu_ly_o_dich` — Biện pháp xử lý *(Điều 24.1, 9 nhóm a–i)*
`id, o_dich_id FK, loai_bien_phap [xu_ly_nguon_benh|xu_ly_duong_truyen|bao_ve_nguoi_dan|truyen_thong|khu_trung|dieu_tra_xu_ly_tu_vong|phoi_hop_lien_nganh_quoc_te|khoanh_vung_kiem_soat|ra_soat_sau_dap_ung], ngay_trien_khai, mo_ta`

---

## PHẦN E. BÁO CÁO – THỐNG KÊ TỔNG HỢP *[Đề xuất kỹ thuật]*
- `dm_chi_tieu`: `id, ma_chi_tieu, ten_chi_tieu, mau_bao_cao, linh_vuc='benh_truyen_nhiem', don_vi_tinh, cong_thuc` — danh mục chỉ tiêu tổng hợp tình hình dịch.
- `bc_chi_tieu_thong_ke`: fact-table số mắc/tử vong theo `chi_tieu_id, don_vi_bao_cao_id, ky_bao_cao, nam, thang, phan_to_gioi_tinh, phan_to_nhom_tuoi, phan_to_khac (bệnh/tuyến/địa bàn), gia_tri_so_luong, gia_tri_ty_le, nguon_tinh_toan, ngay_chot_so_lieu, trang_thai_gui`.
- `bc_luong_bao_cao`: giám sát tuân thủ thời hạn báo cáo — `id, don_vi_gui_id FK, don_vi_nhan_id FK, linh_vuc='benh_truyen_nhiem', ky_bao_cao_id FK, han_gui, ngay_gui_thuc_te, trang_thai [dung_han|tre_han|chua_gui]`.

---

## PHẦN F. MA TRẬN LUỒNG BÁO CÁO (bệnh truyền nhiễm)
| Nội dung | Đơn vị gửi | Đơn vị nhận | Kỳ hạn | Căn cứ |
|---|---|---|---|---|
| Phát hiện nghi ngờ mắc bệnh | Cơ quan/tổ chức/cá nhân | Trạm Y tế cấp xã | 24h | Điều 10.1 |
| Ca bệnh | TYT xã/CSKCB/CS xét nghiệm | Hệ thống TT giám sát (trực tuyến) | 24h / 48h / tuần (theo Danh mục 01) | Điều 10.2, Danh mục 01 PL I |
| Tử vong do/nghi do BTN | CSKCB / TYT xã | Hệ thống | 24h (từ khi tử vong tại CSKCB / hoàn thành xác minh tại cộng đồng) | Điều 10.2b |
| Tổng hợp tình hình | TTKSBT tỉnh | CQ chuyên môn y tế tỉnh + 1 trong 6 Viện theo địa bàn | theo hướng dẫn CPB | Điều 10.3 |
| Vùng → TW | 6 Viện khu vực | Viện VSDT TW / Viện SR-KST-CT TW | | Điều 10.4 |
| TW → Cục | Viện VSDT TW, SR-KST-CT TW, BV Phổi TW | Cục Phòng bệnh (+ Cục QLKCB cho lao) | | Điều 10.5–6 |
| Có dịch / hết dịch | TYT xã | Chủ tịch UBND xã, CQ chuyên môn y tế tỉnh, TTKSBT tỉnh, lực lượng chuyên trách | 24h kể từ khi xác định; báo cáo ổ dịch hằng ngày đến khi kết thúc | Điều 26.1 |

---

## PHẦN G. RÀNG BUỘC NGHIỆP VỤ
1. **Phân loại nhóm A/B/C** (Điều 14–15, PL I TT15): `tong_diem = Σ 4 tiêu chí`; A nếu ≥10 hoặc "ĐBNH mới phát sinh chưa rõ tác nhân"; B nếu 7–9; C nếu <7. Cài bằng trigger/computed, không nhập tay `nhom_phan_loai`.
2. **Xác định có dịch cấp xã** (Điều 16.1): nhóm A theo hướng dẫn riêng từng bệnh (cần bảng ngưỡng riêng khi CPB ban hành); nhóm B/C lưu hành: `số mắc cộng dồn tháng > TB 5 năm cùng kỳ + 2×độ lệch chuẩn`; nhóm B/C không lưu hành: `≥5 ca cộng dồn có liên quan dịch tễ`.
3. **Cảnh báo dịch** (Điều 22.1): ngưỡng theo tuần, hệ số 1–2×độ lệch chuẩn; nhóm B/C không lưu hành ngưỡng 3 ca liên quan dịch tễ (thấp hơn ngưỡng "có dịch").
4. **Cấp độ PTDS** (Điều 17–19): điều kiện lồng nhau cấp xã→tỉnh→liên tỉnh; mỗi cấp kiểm 3 điều kiện; lưu vết ở `btn_cap_do_phong_thu_dan_su`.
5. **Toàn vẹn ICD-10**: mã ICD-10 phải thuộc `dm_benh_truyen_nhiem_icd10`; cho phép NULL (bệnh chưa có mã) nhưng bắt buộc `benh_id` khớp danh mục (ghi chú Danh mục 01 PL I).
6. **Kỳ hạn báo cáo**: cảnh báo trễ hạn khi `ngay_gui_thuc_te > han_gui` (bảng F).

---

## PHẦN H. PHÂN QUYỀN & AN TOÀN DỮ LIỆU (Điều 3.3)
- `ht_nguoi_dung (id, ho_ten, ma_dinh_danh, don_vi_id FK)`
- `ht_vai_tro (id, ten_vai_tro)` — Nhân viên TYT xã / Cán bộ TTKSBT tỉnh / Cán bộ Viện / Cán bộ Cục Phòng bệnh / Quản trị hệ thống.
- `ht_phan_quyen (vai_tro_id, chuc_nang, muc_do [xem|nhap|sua|duyet|xuat])` — giới hạn theo `don_vi_id` và cấp quản lý trong cây `dm_don_vi`.
- `ht_nhat_ky_truy_cap (id, nguoi_dung_id, hanh_dong, doi_tuong, thoi_gian, dia_chi_ip)` — audit log.
- Dữ liệu định danh (`nguoi.so_dinh_danh_ca_nhan`, họ tên, địa chỉ, tiền sử dịch tễ) mã hóa tại chỗ; báo cáo lên cấp cao hơn ở dạng tổng hợp/ẩn danh.

---

## PHẦN I. TÓM TẮT DANH SÁCH BẢNG (33 bảng)
| Nhóm | Số bảng | Bảng |
|---|---|---|
| Danh mục dùng chung | 13 | dm_dia_ban_hanh_chinh, dm_loai_don_vi, dm_don_vi, dm_dia_ban_phu_trach, dm_benh_truyen_nhiem, dm_benh_truyen_nhiem_icd10, dm_nghe_nghiep, dm_dan_toc, dm_muc_do_nguy_co_dot_xuat, dm_cap_do_phong_thu_dan_su, dm_loai_hinh_giam_sat, dm_ky_bao_cao, nguoi |
| Bệnh truyền nhiễm | 13 | btn_doi_tuong_giam_sat, btn_truong_hop_benh, btn_o_dich, btn_o_dich_so_lieu_ngay, btn_o_dich_tong_hop, btn_bao_cao_dich_benh, btn_bao_cao_dich_benh_chi_tiet, btn_khai_bao_ca_nhan, btn_danh_gia_nguy_co, btn_canh_bao_dich_benh, btn_cap_do_phong_thu_dan_su, btn_dieu_tra_o_dich, btn_bien_phap_xu_ly_o_dich |
| Báo cáo – thống kê | 3 | dm_chi_tieu, bc_chi_tieu_thong_ke, bc_luong_bao_cao |
| Hệ thống | 4 | ht_nguoi_dung, ht_vai_tro, ht_phan_quyen, ht_nhat_ky_truy_cap |

---

## PHẦN J. CHUẨN MÃ HÓA DỮ LIỆU
| Trường / miền | Chuẩn Việt Nam | Cấu trúc mã |
|---|---|---|
| `nguoi.so_dinh_danh_ca_nhan` | Luật Căn cước 2023; NĐ 137/2015 (sửa đổi NĐ 37/2021) | 12 chữ số |
| `nguoi.ma_dinh_danh_y_te` | Quyết định 2153/QĐ-BYT | = số định danh cá nhân |
| `nguoi.gioi_tinh` | Quyết định 4210/QĐ-BYT (GIOITINH) | 1=Nam; 2=Nữ; 3=Chưa xác định |
| `nguoi.dan_toc_id` | Quyết định 4210/QĐ-BYT (DANTOC) | 2 chữ số (54 dân tộc) |
| `nguoi.quoc_tich` | QĐ 4210/QĐ-BYT (QUOCGIA) / ISO 3166-1 alpha-3 | 3 ký tự (vd VNM) |
| `nguoi.nghe_nghiep_id` | QĐ 4210/QĐ-BYT (NGHENGHIEP) | mã danh mục |
| `dm_dia_ban_hanh_chinh.ma_dia_ban` | **Quyết định 19/2025/QĐ-TTg** | tỉnh 2 số; xã 5 số |
| `dm_don_vi.ma_don_vi` | Quyết định 5937/QĐ-BYT | mã cơ sở KCB |
| Mã bệnh (ICD-10) | **Thông tư 06/2026/TT-BYT** | ICD-10 (A80, A20, J09...) |
| Nhóm bệnh A/B/C | Điều 15 + PL I TT15 | A/B/C theo điểm |
| Kỳ hạn báo cáo | Danh mục 01 PL I QĐ97 | 24h/48h/tuần |

**Kết luận rà soát mã:** mã ICD-10 đã đối chiếu khớp bản gốc QĐ97; mã hành chính theo QĐ 19/2025/QĐ-TTg (2 cấp); giới tính/dân tộc/quốc gia/nghề nghiệp theo QĐ 4210/QĐ-BYT; số định danh cá nhân theo Luật Căn cước 2023 (đồng thời là mã định danh y tế QĐ 2153/QĐ-BYT).

---

## PHỤ LỤC: ĐỐI CHIẾU CĂN CỨ PHÁP LÝ ↔ BẢNG
| Điều / Mẫu | Bảng |
|---|---|
| Điều 5 | btn_doi_tuong_giam_sat |
| Điều 6–9 | dm_loai_hinh_giam_sat |
| Điều 10, Mẫu 01 PL I | btn_truong_hop_benh |
| Điều 12–13 | btn_khai_bao_ca_nhan |
| Điều 14–15, PL I TT15 | dm_benh_truyen_nhiem |
| Điều 16 | quy tắc G.2 + btn_o_dich.trang_thai |
| Điều 17–20 | btn_cap_do_phong_thu_dan_su |
| Điều 21 | btn_danh_gia_nguy_co |
| Điều 22 | btn_canh_bao_dich_benh |
| Điều 23 | btn_dieu_tra_o_dich |
| Điều 24 | btn_bien_phap_xu_ly_o_dich |
| Điều 25–26, Mẫu 01/02 PL II | btn_bao_cao_dich_benh |
| Mẫu 02, 03 PL I | btn_o_dich, btn_o_dich_so_lieu_ngay, btn_o_dich_tong_hop |
| Mẫu 04, 05 PL I | btn_bao_cao_dich_benh_chi_tiet |
| Danh mục 01 PL I | dm_benh_truyen_nhiem, dm_benh_truyen_nhiem_icd10 |
| Điều 3.3 | ht_nguoi_dung, ht_vai_tro, ht_phan_quyen, ht_nhat_ky_truy_cap |
