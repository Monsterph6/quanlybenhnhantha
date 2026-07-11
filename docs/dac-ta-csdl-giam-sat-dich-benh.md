# ĐẶC TẢ CƠ SỞ DỮ LIỆU GIÁM SÁT DỊCH BỆNH

**Căn cứ pháp lý:**
- Thông tư số 15/2026/TT-BYT ngày 17/5/2026 của Bộ trưởng Bộ Y tế quy định chi tiết một số điều của Luật Phòng bệnh số 114/2025/QH15 (hiệu lực từ 01/7/2026).
- Quyết định số 97/QĐ-PB ngày 30/6/2026 của Cục trưởng Cục Phòng bệnh ban hành các danh mục, mẫu giám sát, mẫu báo cáo chuyên môn thực hiện Thông tư 15/2026/TT-BYT (Phụ lục I, II, III, IV).

**Phạm vi:** Toàn bộ 5 mảng giám sát trong phòng bệnh theo Thông tư 15/2026/TT-BYT: (1) Bệnh truyền nhiễm, (2) Bệnh không lây nhiễm, (3) Rối loạn tâm thần, (4) Dinh dưỡng trong phòng bệnh, (5) Dự phòng thương tích tại cộng đồng.

**Ghi chú về nguồn:** Mọi bảng, trường dữ liệu trong đặc tả này được ánh xạ trực tiếp tới Điều/Khoản của Thông tư 15/2026/TT-BYT hoặc Mẫu/Phụ lục của Quyết định 97/QĐ-PB (ghi trong cột "Căn cứ" hoặc ngay dưới tên bảng). Phần nào là đề xuất kỹ thuật thuần túy (không có trong văn bản, do người thiết kế CSDL bổ sung để đảm bảo tính toàn vẹn/vận hành hệ thống) được đánh dấu **[Đề xuất kỹ thuật]**.

---

## PHẦN A. TỔNG QUAN

### A.1. Mục tiêu hệ thống

Theo Điều 3 TT15/2026/TT-BYT, Hệ thống thông tin giám sát trong phòng bệnh có chức năng: **tiếp nhận, cập nhật, quản lý, tổng hợp, phân tích, khai thác, phản hồi, chia sẻ dữ liệu** và hỗ trợ thực hiện chế độ thông tin, báo cáo giám sát về: bệnh truyền nhiễm, bệnh không lây nhiễm, rối loạn tâm thần, dinh dưỡng trong phòng bệnh, thương tích tại cộng đồng.

### A.2. Mô hình phân cấp đơn vị (áp dụng chung cho cả 5 mảng)

```
Cấp xã           : Trạm Y tế cấp xã (TYT), Cơ sở khám bệnh chữa bệnh (CSKCB),
                    Cơ sở xét nghiệm, Cơ sở giáo dục, Cơ sở bảo trợ xã hội,
                    Tổ chức kiểm dịch y tế tại cửa khẩu
Cấp tỉnh          : Cơ quan chuyên môn về y tế thuộc UBND cấp tỉnh (Sở Y tế),
                    Trung tâm Kiểm soát bệnh tật cấp tỉnh (TTKSBT/CDC),
                    Trung tâm Kiểm dịch y tế quốc tế
Cấp vùng/Viện     : Viện Vệ sinh dịch tễ Trung ương, Viện Vệ sinh dịch tễ Tây Nguyên,
                    Viện Pasteur TP.HCM, Viện Pasteur Nha Trang,
                    Viện Sốt rét - KST - Côn trùng Trung ương/Quy Nhơn/TP.HCM,
                    Viện Dinh dưỡng, Viện Sức khỏe nghề nghiệp và Môi trường,
                    Viện Y tế công cộng TP.HCM
Cấp Trung ương    : Cục Phòng bệnh (đầu mối quốc gia), Cục Quản lý Khám chữa bệnh,
                    Bệnh viện Phổi Trung ương (đầu mối bệnh lao),
                    Các Bệnh viện trực thuộc Bộ Y tế (đầu mối quốc gia theo phân công)
```
→ Bảng `dm_don_vi` (mục C.2) mô hình hoá cấu trúc cây này bằng quan hệ đệ quy `don_vi_cha_id` + `dm_loai_don_vi` + `dm_dia_ban_phu_trach` (địa bàn phụ trách của các Viện theo Điều 10 khoản 3).

### A.3. Ba loại hình giám sát bệnh truyền nhiễm (Điều 6)

| Loại hình | Điều | Mô tả |
|---|---|---|
| Giám sát dựa vào chỉ số | Điều 6.1, 7 | Thu thập thường xuyên, liên tục, toàn quốc |
| Giám sát trọng điểm | Điều 6.2, 8 | Thu thập chuyên sâu tại điểm giám sát được chọn, theo kế hoạch quốc gia/tỉnh |
| Giám sát dựa vào sự kiện | Điều 6.3, 9 | Thu thập/sàng lọc/xác minh tín hiệu từ cộng đồng, mạng xã hội, CSKCB, ngành NN&MT |

### A.4. Nguyên tắc thiết kế CSDL

1. **Tách dữ liệu vi mô (case-level) khỏi dữ liệu tổng hợp (aggregate):** các bảng nghiệp vụ lưu từng trường hợp/đối tượng cụ thể (người bệnh, ca bệnh, ổ dịch...); các "Mẫu báo cáo" tổng hợp theo kỳ (tháng/quý/6 tháng/năm) trong QĐ 97 phần lớn là **kết quả tính toán (aggregation)** từ dữ liệu vi mô, không cần lưu trùng lặp — xem mô hình `bc_chi_tieu_thong_ke` ở Phần E. **[Đề xuất kỹ thuật]**
2. **Danh mục dùng chung tập trung:** mọi mã bệnh/ICD-10/nguyên nhân/nhóm phân loại lấy từ Phụ lục I–IV QĐ 97, không hard-code trong ứng dụng.
3. **Truy vết đơn vị & luồng báo cáo:** mọi bản ghi nghiệp vụ có `don_vi_id` (đơn vị tạo/quản lý) để tái dựng đúng luồng báo cáo theo cấp quy định tại Điều 10, 11, 26, 33, 40, 46, 47, 53.
4. **An toàn dữ liệu cá nhân:** theo Điều 3 khoản 3 TT15, việc quản lý/cập nhật/trích xuất/chia sẻ phải theo pháp luật về an toàn thông tin mạng, an ninh mạng, bảo vệ dữ liệu cá nhân → xem Phần I (phân quyền, mã hoá, nhật ký truy cập).
5. **Định danh cá nhân:** dùng số định danh cá nhân/CCCD/hộ chiếu làm khoá tra cứu chính cho đối tượng (person), tách bảng `nguoi` dùng chung giữa các mảng thay vì lặp lại thông tin nhân khẩu ở từng bảng chuyên đề. **[Đề xuất kỹ thuật]**

---

## PHẦN B. QUY ƯỚC CHUNG

- Đặt tên bảng/trường: chữ thường, không dấu, phân tách `_`, tiền tố theo miền nghiệp vụ:
  `dm_` danh mục dùng chung · `btn_` bệnh truyền nhiễm · `kln_` bệnh không lây nhiễm & rối loạn tâm thần · `dd_` dinh dưỡng · `tt_` thương tích · `bc_` báo cáo/thống kê dùng chung · `ht_` hệ thống/quản trị.
- Khoá chính: `id BIGINT` tự tăng (hoặc `UUID`), mọi bảng nghiệp vụ có cột chuẩn:
  `don_vi_id` (đơn vị sở hữu bản ghi), `nguoi_tao_id`, `ngay_tao`, `nguoi_cap_nhat_id`, `ngay_cap_nhat`, `trang_thai` (nháp/đã gửi/đã duyệt/đã huỷ).
- Kiểu dữ liệu mô tả theo ANSI SQL chuẩn (VARCHAR, INT, DATE, DATETIME, DECIMAL, BOOLEAN, TEXT); khi triển khai cụ thể ánh xạ sang PostgreSQL/SQL Server/MySQL/Oracle.
- Ký hiệu bắt buộc: **PK** khoá chính · **FK** khoá ngoại · **NN** NOT NULL · **UQ** duy nhất.

---

## PHẦN C. DANH MỤC DÙNG CHUNG (DM_*)

### C.1. `dm_dia_ban_hanh_chinh` — Danh mục đơn vị hành chính (tỉnh/xã)
*[Đề xuất kỹ thuật — nền tảng địa bàn dùng cho mọi báo cáo theo Điều 16 (cấp xã), theo tỉnh]*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| ma_dia_ban | VARCHAR(10) | UQ, NN | Mã hành chính (theo danh mục Bộ Nội vụ) |
| ten_dia_ban | VARCHAR(200) | NN | Tên xã/phường/đặc khu hoặc tỉnh/thành phố |
| cap | VARCHAR(10) | NN | `xa` \| `tinh` (mô hình chính quyền 2 cấp) |
| dia_ban_cha_id | BIGINT | FK→ chính bảng | Tỉnh cha (nếu cấp = xã) |

### C.2. `dm_don_vi` — Danh mục đơn vị/cơ sở y tế
*Căn cứ: Điều 10, 33, 40, 46, 47, 53, 54–64 (danh sách đơn vị tham gia hệ thống báo cáo)*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| ma_don_vi | VARCHAR(20) | UQ, NN | Mã đơn vị |
| ten_don_vi | VARCHAR(300) | NN | |
| loai_don_vi_id | BIGINT | FK→dm_loai_don_vi, NN | |
| dia_ban_id | BIGINT | FK→dm_dia_ban_hanh_chinh | Xã/tỉnh quản lý địa bàn |
| don_vi_cha_id | BIGINT | FK→ chính bảng | Đơn vị quản lý trực tiếp (mô hình cây báo cáo) |
| dia_chi | VARCHAR(500) | | |
| dien_thoai, email | VARCHAR | | |
| trang_thai_hoat_dong | BOOLEAN | NN | |

### C.3. `dm_loai_don_vi` — Danh mục loại hình đơn vị
Giá trị cố định theo văn bản: `tram_y_te_xa`, `cskcb` (cơ sở khám bệnh, chữa bệnh), `cs_xet_nghiem`, `so_y_te`/`cq_chuyen_mon_yte_tinh`, `ttksbt_tinh`, `tt_kiem_dich_yt_quoc_te`, `vien_vsdt_pasteur`, `vien_sot_ret_kst_con_trung`, `vien_dinh_duong`, `vien_suc_khoe_nghe_nghiep_moi_truong`, `vien_yte_cong_cong`, `benh_vien_tw`, `benh_vien_phoi_tw`, `cuc_phong_benh`, `cuc_ql_kham_chua_benh`, `co_so_giao_duc`, `co_so_bao_tro_xa_hoi`, `to_chuc_kiem_dich_yt_cua_khau`.

### C.4. `dm_dia_ban_phu_trach` — Phân công địa bàn phụ trách của các Viện
*Căn cứ: Điều 10.3 (VSDT/Pasteur/SR-KST-CT), Điều 46.2b (Viện Dinh dưỡng, Pasteur Nha Trang, VSDT Tây Nguyên, Viện YTCC TP.HCM), Điều 53.4 (Viện SKNN&MT + 3 viện khác)*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| vien_id | BIGINT | FK→dm_don_vi, NN | |
| tinh_id | BIGINT | FK→dm_dia_ban_hanh_chinh, NN | |
| linh_vuc | VARCHAR(30) | NN | `benh_truyen_nhiem`\|`khong_lay_nhiem`\|`roi_loan_tam_than`\|`dinh_duong`\|`thuong_tich` |

### C.5. `dm_benh_truyen_nhiem` — Danh mục bệnh truyền nhiễm
*Căn cứ: Danh mục 01 – Phụ lục I QĐ97 (46 bệnh) + Điều 14, 15, Phụ lục I TT15 (phân loại điểm số)*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| ma_benh | VARCHAR(20) | UQ, NN | Mã nội bộ |
| ten_benh | VARCHAR(300) | NN | |
| nhom_phan_loai | CHAR(1) | NN, CHECK IN ('A','B','C') | Theo Điều 15 |
| ky_han_bao_cao | VARCHAR(20) | NN | `24h`\|`48h`\|`tuan` — theo Danh mục 01 PL I QĐ97 |
| diem_muc_do_nghiem_trong | TINYINT | CHECK 1..3 | Tiêu chí 1 – Phụ lục I TT15 |
| diem_kha_nang_lay_lan | TINYINT | CHECK 1..3 | Tiêu chí 2 |
| diem_can_thiep_vacxin_thuoc | TINYINT | CHECK 1..3 | Tiêu chí 3 |
| diem_muc_do_luu_hanh_tiem_nang_dich | TINYINT | CHECK 1..3 | Tiêu chí 4 |
| tong_diem | TINYINT | tính toán = tổng 4 tiêu chí (4–12) | Quy tắc: A nếu ≥10 hoặc "đặc biệt nguy hiểm mới phát sinh chưa rõ tác nhân"; B nếu 7–9; C nếu <7 |
| luu_hanh_tai_dia_phuong | BOOLEAN | | Có lưu hành ổn định hay không — dùng cho quy tắc xác định dịch (Điều 16.1.b/c) |
| ghi_chu | TEXT | | |

`dm_benh_truyen_nhiem_icd10` (1-n): `id`, `benh_id` FK, `ma_icd10` VARCHAR(10) — một bệnh có thể có nhiều mã ICD-10 (vd cúm A(H5N1)/(H5N6)/(H7N9)/(H9N2) đều dùng J09 nhưng khác bệnh; các bệnh khác như "Bệnh do vi rút Adeno khác" có nhiều mã).

### C.6. `dm_benh_khong_lay_nhiem` — Danh mục bệnh không lây nhiễm
*Căn cứ: Mục I.1 – Phụ lục II QĐ97 (6 bệnh phổ biến nhóm A + 19 bệnh khác nhóm B)*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| ma_benh | VARCHAR(20) | UQ | |
| ten_benh | VARCHAR(300) | NN | |
| nhom | VARCHAR(20) | NN | `pho_bien` (6 bệnh: THA, ĐTĐ, COPD, Hen phế quản, Ung thư, Bệnh mạch máu não) \| `khac` (19 bệnh) |
| nhom_benh_theo_he_co_quan | VARCHAR(100) | | Vd "Bệnh hệ tuần hoàn", "Bệnh hệ tiết niệu"... (theo bảng phân nhóm PL II) |
| co_mau_so_rieng | BOOLEAN | | TRUE cho 4 bệnh có sổ/báo cáo riêng: THA, ĐTĐ, COPD/Hen, (Ung thư và Bệnh mạch máu não dùng sổ 04 chung) |

`dm_benh_khong_lay_nhiem_icd10`: `id`, `benh_id` FK, `ma_icd10_tu`, `ma_icd10_den` (hỗ trợ khoảng mã, vd I10-I15).

### C.7. `dm_roi_loan_tam_than` — Danh mục rối loạn tâm thần
*Căn cứ: Mục I.2 – Phụ lục II QĐ97 (3 rối loạn phổ biến + 11 rối loạn khác, mã F00–F99)*

Cấu trúc tương tự C.6: `id, ma_benh, ten_benh, nhom` (`pho_bien`: Tâm thần phân liệt F20/Rối loạn trầm cảm F32-33/Sa sút trí tuệ F00-03; `khac`: 11 nhóm F04-F99), + bảng con `dm_roi_loan_tam_than_icd10`.

### C.8. `dm_nguyen_nhan_thuong_tich` — Danh mục 13 nguyên nhân thương tích
*Căn cứ: Hướng dẫn ghi Cột 12 – Mẫu 01/02 Phụ lục IV QĐ97; đối chiếu mã ICD-10 tại Mẫu 08 PL IV*

| ma | ten_nguyen_nhan | ma_icd10_tu_den |
|---|---|---|
| 1 | Tai nạn giao thông | V01–V99 |
| 2 | Tai nạn lao động | W20–W49 |
| 3 | Đuối nước | W65–W74 |
| 4 | Ngã | W00–W19 |
| 5 | Bỏng (cháy nổ, nhiệt, hoá chất) | X00–X19, W36–W40, W88–W99 |
| 6 | Hóc, sặc dị vật | W75–W84 |
| 7 | Ngộ độc (hoá chất/thực phẩm/động-thực vật có độc) | X20–X29, X40–X49 |
| 8 | Bạo lực | X85–Y09 |
| 9 | Tự tử | X60–X84 |
| 10 | Súc vật, động vật cắn, đốt, tấn công | W50–W64 |
| 11 | Điện giật | W85–W87 |
| 12 | Thương tích do thiên tai (bão lụt, sạt lở, sét đánh) | X30–X39 |
| 13 | Thương tích không rõ nguyên nhân | X59 |

Bảng: `id, ma (1-13), ten_nguyen_nhan, ma_icd10_tu, ma_icd10_den` (bảng con nếu nhiều khoảng mã cho 1 nguyên nhân, như mã 5, 7).

### C.9. Danh mục nhỏ khác **[đa số Đề xuất kỹ thuật, chuẩn hoá từ giá trị liệt kê trong mẫu]**

- `dm_nghe_nghiep`: Cán bộ công chức, Nông dân, Bộ đội/công an, Trẻ em (0–4 tuổi), Học sinh/sinh viên, Công nhân/thợ thủ công, Lao động tự do/buôn bán, Nghề khác *(theo Mẫu 01 PL IV)*.
- `dm_dan_toc`: theo danh mục 54 dân tộc Việt Nam (chuẩn quốc gia hiện hành, không nằm trong TT15/QĐ97 nhưng bắt buộc để điền cột "Dân tộc" — Mẫu 01 PL III).
- `dm_dia_diem_xay_ra_thuong_tich`: Hộ gia đình / Cơ sở giáo dục / Khu vực công cộng *(Cột 10 Mẫu 01/02 PL IV)*.
- `dm_bo_phan_bi_thuong`: Đầu-mặt-cổ / Thân mình / Chi / Đa chấn thương / Khác.
- `dm_muc_do_thuong_tich`: Nhẹ / Trung bình / Nặng *(định nghĩa chi tiết ở Cột 13 Mẫu 01 PL IV, lưu trong `mo_ta`)*.
- `dm_yeu_to_nguy_co_thuong_tich_mau`: danh mục tham khảo 12 loại hình thương tích × yếu tố môi trường/hành vi/khác *(Mẫu 06, 07 PL IV — dùng làm gợi ý nhập liệu, không phải bảng giao dịch)*.
- `dm_muc_do_nguy_co_dot_xuat`: Thấp / Trung bình / Cao / Rất cao *(Điều 21.2)*.
- `dm_cap_do_phong_thu_dan_su`: 1 / 2 / 3 / Tình trạng khẩn cấp *(Điều 17–20)*.
- `dm_loai_hinh_giam_sat`: Dựa vào chỉ số / Trọng điểm / Dựa vào sự kiện *(Điều 6)*.
- `dm_ky_bao_cao`: Tháng / 6 tháng / Năm / Định kỳ 5 năm / Đột xuất.

---

## PHẦN D. BẢNG DỮ LIỆU NGHIỆP VỤ (theo miền)

### D.0. `nguoi` — Hồ sơ cá nhân dùng chung
*[Đề xuất kỹ thuật — hợp nhất trường nhân khẩu lặp lại ở mọi mẫu sổ/báo cáo (Cột 1–8 các Mẫu sổ PL II, PL III, PL IV đều giống nhau)]*

| Trường | Kiểu | Ràng buộc | Mô tả | Căn cứ |
|---|---|---|---|---|
| id | BIGINT | PK | |
| ho_ten | VARCHAR(200) | NN | | Mẫu 01 PL I; các mẫu sổ |
| so_dinh_danh_ca_nhan | VARCHAR(20) | UQ | CCCD/CC/hộ chiếu | Mẫu 01 PL I |
| ngay_sinh | DATE | | Có thể chỉ có năm sinh | |
| gioi_tinh | VARCHAR(10) | CHECK IN('nam','nu','khong_xac_dinh') | | Mẫu 01 PL I |
| dan_toc_id | BIGINT | FK→dm_dan_toc | | |
| quoc_tich | VARCHAR(100) | | | Mẫu 01 PL I |
| nghe_nghiep_id | BIGINT | FK→dm_nghe_nghiep | | |
| dien_thoai | VARCHAR(20) | | |
| dia_chi_hien_tai | VARCHAR(500) | | Số nhà, đường/tổ/thôn, phường/xã, tỉnh |
| dia_chi_thuong_tru | VARCHAR(500) | | |
| dia_ban_id | BIGINT | FK→dm_dia_ban_hanh_chinh | Xã quản lý (dùng để tổng hợp báo cáo theo địa bàn dân cư, Điều 33 nguyên tắc "thống kê theo địa bàn dân cư") |
| noi_lam_viec_hoc_tap | VARCHAR(300) | | |

### D.1. MIỀN BỆNH TRUYỀN NHIỄM

#### D.1.1. `btn_doi_tuong_giam_sat`
*Căn cứ: Điều 5 (đối tượng), Điều 7.1a (nội dung giám sát hành chính)*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| nguoi_id | BIGINT | FK→nguoi, NN | |
| loai_doi_tuong | VARCHAR(30) | NN | `mac_benh`\|`mang_mam_benh`\|`nghi_ngo`\|`tiep_xuc`\|`tu_vong_do_hoac_nghi_ngo` (Điều 5.1) |
| don_vi_phat_hien_id | BIGINT | FK→dm_don_vi, NN | |
| ngay_phat_hien | DATETIME | NN | |

#### D.1.2. `btn_truong_hop_benh` — Báo cáo trường hợp bệnh
*Căn cứ: **Mẫu 01 – Phụ lục I QĐ97**; Điều 10.2a TT15*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| doi_tuong_giam_sat_id | BIGINT | FK→btn_doi_tuong_giam_sat, NN | |
| benh_id | BIGINT | FK→dm_benh_truyen_nhiem, NN | |
| phan_loai_bao_cao | VARCHAR(10) | NN | `24h`\|`48h`\|`tuan` |
| tinh_trang_tiem_chung | VARCHAR(10) | | `co`\|`khong`\|`khong_ro` |
| so_lan_tiem | INT | | Nếu `tinh_trang_tiem_chung = co` |
| phan_loai_chan_doan | VARCHAR(20) | NN | `lam_sang_nghi_ngo`\|`xac_dinh_ptn` |
| ngay_khoi_phat | DATE | | |
| da_lay_mau_xn | BOOLEAN | | |
| loai_xet_nghiem | VARCHAR(30) | | `test_nhanh`\|`huyet_thanh_hoc`\|`pcr_rtpcr`\|`khac` |
| ket_qua_xet_nghiem | VARCHAR(20) | | `duong_tinh`\|`am_tinh`\|`nghi_ngo`\|`chua_co_ket_qua` |
| tinh_trang_dieu_tri | VARCHAR(20) | | `ngoai_tru`\|`noi_tru` |
| ngay_nhap_vien | DATE | | |
| ngay_ra_vien_chuyen_vien_tu_vong | DATE | | |
| ket_qua_cuoi | VARCHAR(20) | | `ra_vien`\|`chuyen_vien`\|`tu_vong`\|`khac` |
| tien_su_dich_te | TEXT | | Đi lại, tiếp xúc người bệnh/nghi ngờ, tiếp xúc động vật/gia cầm, phơi nhiễm khác |
| nguoi_bao_cao_id | BIGINT | FK→ht_nguoi_dung | |
| don_vi_bao_cao_id | BIGINT | FK→dm_don_vi, NN | Trạm Y tế xã / CSKCB / cơ sở xét nghiệm |
| o_dich_id | BIGINT | FK→btn_o_dich | Liên kết nếu ca bệnh thuộc 1 ổ dịch (Mẫu 02 PL I) |

#### D.1.3. `btn_o_dich` — Ổ dịch
*Căn cứ: Điều 2.1 (định nghĩa), **Mẫu 02, 03 – Phụ lục I QĐ97***

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| ten_o_dich | VARCHAR(300) | NN | |
| benh_id | BIGINT | FK→dm_benh_truyen_nhiem, NN | |
| don_vi_id | BIGINT | FK→dm_don_vi (Trạm Y tế xã), NN | |
| dia_diem | VARCHAR(500) | NN | Thôn/tổ, xã, tỉnh |
| ngay_khoi_phat_ca_dau | DATE | | |
| ngay_nhap_canh | DATE | | Nếu ca khởi phát ở nước ngoài |
| ngay_den_dia_phuong | DATE | | Bổ sung nếu khởi phát tại nước ngoài |
| ngay_nhan_bao_cao_dau | DATE | NN | |
| ngay_khoi_phat_ca_cuoi | DATE | | Cập nhật khi kết thúc ổ dịch |
| ngay_ket_thuc_hoat_dong | DATE | | |
| mo_ta_yeu_to_nguy_co | TEXT | | |
| trang_thai | VARCHAR(20) | NN | `dang_hoat_dong`\|`da_ket_thuc` |

`btn_o_dich_so_lieu_ngay` (1-n, theo Mẫu 02 mục 2, 3):
`id, o_dich_id FK, ngay DATE, thon_to VARCHAR, so_mac INT, so_tu_vong INT, so_mau_lam_xn INT, so_xn_duong_tinh INT`

`btn_o_dich_tong_hop` (chốt số liệu khi kết thúc — Mẫu 03 mục 7):
`o_dich_id FK, tong_so_mac INT, tong_so_tu_vong INT, tong_so_mau_xn INT, tong_so_mau_duong_tinh INT`

#### D.1.4. `btn_bao_cao_dich_benh` — Thông tin/Báo cáo có dịch – kết thúc dịch
*Căn cứ: Điều 25, 26; **Mẫu 01/02 – Phụ lục II TT15** (thông tin ngắn cấp xã ban hành công khai) và **Mẫu 04/05 – Phụ lục I QĐ97** (báo cáo dịch bệnh đầy đủ)*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| o_dich_id | BIGINT | FK→btn_o_dich | |
| don_vi_id | BIGINT | FK→dm_don_vi (TYT xã), NN | |
| loai_thong_tin | VARCHAR(10) | NN | `co_dich`\|`het_dich` |
| ten_dich_benh | VARCHAR(300) | NN | Điều 25.1a/2a |
| thoi_gian_xac_dinh | DATE | NN | Điều 25.1b (có dịch) |
| thoi_gian_het_dich | DATE | | Điều 25.2b |
| dia_diem_o_dich | VARCHAR(500) | | Điều 25.1c |
| khuyen_nghi | TEXT | | Điều 25.1d / 25.2c |
| so_van_ban | VARCHAR(50) | | Số hiệu văn bản Mẫu 01/02 PL II |
| ngay_ban_hanh | DATE | NN | Trong vòng 24 giờ kể từ khi xác định (Điều 26.1b/c) |
| nguoi_ky_id | BIGINT | FK→ht_nguoi_dung | Giám đốc Trạm Y tế cấp xã |
| noi_nhan | TEXT | | Chủ tịch UBND xã, CQ chuyên môn y tế tỉnh, TTKSBT tỉnh, lực lượng chuyên trách/kiêm nhiệm |

`btn_bao_cao_dich_benh_chi_tiet` (nội dung đầy đủ theo Mẫu 04/05 PL I — 8 mục lớn):
`id, bao_cao_id FK, dac_diem_tinh_hinh TEXT, so_mac_tu_vong_so_sanh TEXT, ket_qua_xet_nghiem TEXT, phan_tich_theo_thoi_gian_dia_diem_con_nguoi TEXT, quy_mo_dich_benh TEXT, yeu_to_trung_gian_vec_to TEXT, tinh_hinh_benh_dong_vat TEXT, bien_phap_da_trien_khai TEXT, huy_dong_nguon_luc TEXT, danh_gia_nhan_dinh_du_bao TEXT, kho_khan_ton_tai TEXT, giai_phap_thoi_gian_toi TEXT, de_xuat_kien_nghi TEXT`
*(mỗi mục lưu dạng text tự do theo đúng cấu trúc I–VIII của Mẫu 04/05; nếu cần khai thác số liệu có cấu trúc, tách riêng bảng con theo từng mục — ví dụ số mắc/tử vong nên lấy trực tiếp từ `btn_truong_hop_benh`/`btn_o_dich_so_lieu_ngay` thay vì nhập tay)*

#### D.1.5. `btn_khai_bao_ca_nhan` — Khai báo thông tin bệnh truyền nhiễm
*Căn cứ: Điều 12, 13*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| nguoi_id | BIGINT | FK→nguoi, NN | |
| cach_thuc_khai_bao | VARCHAR(20) | NN | `dien_thoai`\|`truc_tiep`\|`hinh_thuc_khac`\|`ung_dung_dien_tu` |
| don_vi_tiep_nhan_id | BIGINT | FK→dm_don_vi, NN | TYT xã / CSKCB / Tổ chức kiểm dịch y tế cửa khẩu (Điều 13.2) |
| tinh_trang_suc_khoe | TEXT | | |
| tien_su_tiep_xuc_di_chuyen | TEXT | | |
| ngay_khai_bao | DATETIME | NN | |
| ket_qua_xu_ly | TEXT | | Hướng dẫn biện pháp phòng bệnh áp dụng |

#### D.1.6. `btn_danh_gia_nguy_co`
*Căn cứ: Điều 21*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| loai_danh_gia | VARCHAR(20) | NN | `hang_nam`\|`dot_xuat` |
| benh_id | BIGINT | FK→dm_benh_truyen_nhiem | |
| don_vi_id | BIGINT | FK→dm_don_vi, NN | Cơ quan chuyên môn y tế thực hiện |
| ky_danh_gia | INT | | Năm áp dụng (nếu hằng năm) |
| ngay_danh_gia | DATE | NN | (nếu đột xuất) |
| dau_hieu_kich_hoat | VARCHAR(50) | | 8 dấu hiệu Điều 21.2 (a–h), lưu dạng set/CSV hoặc bảng con |
| muc_do_nguy_co | VARCHAR(20) | | `thap`\|`trung_binh`\|`cao`\|`rat_cao` (chỉ áp dụng đột xuất) |
| yeu_to_gia_tang | TEXT | | |
| nang_luc_nguon_luc | TEXT | | |
| bien_phap_de_xuat | TEXT | | |

#### D.1.7. `btn_canh_bao_dich_benh`
*Căn cứ: Điều 22*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| benh_id | BIGINT | FK→dm_benh_truyen_nhiem, NN | |
| don_vi_dia_ban_id | BIGINT | FK→dm_don_vi (TYT xã), NN | |
| dieu_kien_kich_hoat | VARCHAR(20) | NN | `nhom_a_1_ca`\|`nhom_bc_luu_hanh_vuot_nguong`\|`nhom_bc_khong_luu_hanh_3ca`\|`benh_moi_chua_ghi_nhan` (Điều 22.1 a–d) |
| ngay_canh_bao | DATE | NN | |
| noi_dung_nguy_co | TEXT | | Thời gian, địa điểm, phạm vi, quy mô có thể xảy ra |
| bien_phap_phong_chong | TEXT | | |

#### D.1.8. `btn_cap_do_phong_thu_dan_su`
*Căn cứ: Điều 17, 18, 19, 20*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| cap_do | VARCHAR(20) | NN | `cap_1`\|`cap_2`\|`cap_3`\|`khan_cap` |
| dia_ban_id | BIGINT | FK→dm_dia_ban_hanh_chinh, NN | Xã (cấp 1) / tỉnh (cấp 2) / 1-nhiều tỉnh (cấp 3, khẩn cấp) |
| benh_id | BIGINT | FK→dm_benh_truyen_nhiem | |
| ngay_ban_bo | DATE | NN | |
| ngay_bai_bo | DATE | | |
| can_cu_tieu_chi | TEXT | | Ghi rõ tiêu chí đáp ứng theo Điều 17/18/19/20 |

#### D.1.9. `btn_dieu_tra_o_dich` — Nhật ký điều tra 10 bước
*Căn cứ: Điều 23*

`id, o_dich_id FK, buoc VARCHAR(50) [chuan_bi|xac_minh_chan_doan|khang_dinh_ton_tai|dieu_tra_phat_hien_truong_hop|mo_ta_3_yeu_to|xay_dung_gia_thuyet|danh_gia_kiem_dinh|hoan_thien_gia_thuyet|de_xuat_bien_phap|bao_cao_ket_qua], noi_dung TEXT, ngay_thuc_hien DATE, nguoi_thuc_hien_id FK→ht_nguoi_dung`

#### D.1.10. `btn_bien_phap_xu_ly_o_dich`
*Căn cứ: Điều 24.1 (9 nhóm biện pháp a–i)*

`id, o_dich_id FK, loai_bien_phap VARCHAR(30) [xu_ly_nguon_benh|xu_ly_duong_truyen|bao_ve_nguoi_dan|truyen_thong|khu_trung|dieu_tra_xu_ly_tu_vong|phoi_hop_lien_nganh_quoc_te|khoanh_vung_kiem_soat|ra_soat_sau_dap_ung], ngay_trien_khai DATE, mo_ta TEXT`

---

### D.2. MIỀN BỆNH KHÔNG LÂY NHIỄM & RỐI LOẠN TÂM THẦN

*Căn cứ chung: Điều 27–40 TT15; Mẫu sổ 01A–06 và Mẫu báo cáo 01–08 – Phụ lục II QĐ97.*
Thiết kế: 1 bảng hồ sơ người bệnh dùng chung (`kln_nguoi_benh`) + các bảng "lần theo dõi" (visit) chuyên biệt theo bệnh (vì chỉ số theo dõi khác nhau giữa THA/ĐTĐ/COPD-Hen/Tâm thần), + 2 bảng đăng ký người có nguy cơ.

#### D.2.1. `kln_nguoi_benh` — Sổ/hồ sơ người mắc bệnh KLN & RLTT
*Gộp Mẫu sổ 01A, 01B, 02, 03, 04 – Phụ lục II (Cột 1–8 dùng chung; Cột "chẩn đoán" khác nhau theo mẫu)*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| nguoi_id | BIGINT | FK→nguoi, NN | |
| benh_id | BIGINT | FK→dm_benh_khong_lay_nhiem | Loại trừ lẫn nhau với `roi_loan_tam_than_id` |
| roi_loan_tam_than_id | BIGINT | FK→dm_roi_loan_tam_than | |
| loai_so | VARCHAR(10) | NN | `01A_tha`\|`02_copd_hpq`\|`03_tam_than`\|`04_khac` (Mẫu 01B ĐTĐ gộp vào 01A về cấu trúc) |
| co_so_y_te_quan_ly_id | BIGINT | FK→dm_don_vi, NN | |
| noi_chan_doan_dau_id | BIGINT | FK→dm_don_vi | Cột 9 Mẫu sổ 04 |
| ma_icd10_ghi_nhan | VARCHAR(10) | | Cột 11 Mẫu sổ 04 (nếu có) |
| nam_theo_doi | INT | NN | Sổ lập theo từng năm dương lịch (lưu ý QĐ97: "kết thúc 1 năm sẽ lập sổ mới") |
| trang_thai | VARCHAR(20) | NN | `dang_quan_ly`\|`tu_vong`\|`chuyen_di`\|`mat_theo_doi` |
| ghi_chu | TEXT | | |

#### D.2.2. `kln_lan_kham_tha` — Theo dõi tăng huyết áp theo tháng
*Mẫu sổ 01A / Mẫu báo cáo 01 mục 1 PL II*

`id, nguoi_benh_id FK, thang TINYINT(1-12), csyt_quan_ly_id FK→dm_don_vi, ngay_kham DATE, noi_kham_id FK→dm_don_vi, chi_so_huyet_ap_tam_thu INT, chi_so_huyet_ap_tam_truong INT, dat_ha_muc_tieu TINYINT [0=không đạt,1=đạt,2=chưa đánh giá], thuoc_dieu_tri TEXT`

#### D.2.3. `kln_lan_kham_dtd` — Theo dõi đái tháo đường theo tháng
*Mẫu sổ 01B*

`id, nguoi_benh_id FK, thang TINYINT, csyt_quan_ly_id FK, ngay_kham DATE, noi_kham_id FK, duong_mau_mmol_l DECIMAL(4,1), dat_duong_mau_muc_tieu TINYINT [0/1/2], thuoc_dieu_tri TEXT`

#### D.2.4. `kln_lan_kham_copd_hpq` — Theo dõi COPD/hen phế quản theo tháng
*Mẫu sổ 02*

`id, nguoi_benh_id FK, thang TINYINT, csyt_quan_ly_id FK, ngay_kham DATE, noi_kham_id FK, luu_luong_dinh_hoac_fev1 TINYINT [1=tốt,2=trung bình,3=kém], ket_qua_dieu_tri_copd TINYINT [0/1], ket_qua_dieu_tri_hpq TINYINT [0=không kiểm soát,1=một phần,2=đạt mục tiêu], thuoc TEXT`

#### D.2.5. `kln_lan_kham_tam_than` — Theo dõi tâm thần phân liệt/trầm cảm/sa sút trí tuệ theo tháng
*Mẫu sổ 03*

`id, nguoi_benh_id FK, thang TINYINT, csyt_quan_ly_id FK, ngay_kham DATE, noi_kham_id FK, thuoc_dieu_tri TEXT, phuc_hoi_chuc_nang CHAR(2) [K=kém, TB=trung bình, T=tốt]`

#### D.2.6. `kln_nguoi_nguy_co_kln` — Sổ ghi nhận người có nguy cơ mắc bệnh KLN
*Mẫu sổ 05*

`id, nguoi_id FK→nguoi, ngay_kham DATE, noi_kham_id FK→dm_don_vi, chi_so_duong_mau DECIMAL(4,1), chi_so_luu_luong_dinh_fev1 DECIMAL(5,2), ket_qua_dien_tam_do TINYINT [1=có rung nhĩ], ket_qua_via TINYINT [1=dương tính,0=âm tính], ghi_chu TEXT`

#### D.2.7. `kln_nguoi_nguy_co_tam_than` — Sổ ghi nhận người có nguy cơ rối loạn tâm thần
*Mẫu sổ 06*

`id, nguoi_id FK, ngay_kham DATE, noi_kham_id FK, ket_qua_tam_than_phan_liet VARCHAR(100), ket_qua_roi_loan_tram_cam VARCHAR(100), ket_qua_sa_sut_tri_tue VARCHAR(100), bien_phap_can_thiep TEXT`

#### D.2.8. Báo cáo tổng hợp miền KLN/RLTT
Các **Mẫu 01–08 – Phụ lục II QĐ97** (báo cáo tháng/năm của CSKCB, cơ sở bảo trợ XH, TYT xã, TTKSBT tỉnh, Viện) là báo cáo **tổng hợp/đếm số liệu** trên nền `kln_nguoi_benh` + các bảng lần khám → xem mô hình chỉ tiêu thống kê dùng chung Phần E (khuyến nghị chính) hoặc bảng snapshot riêng nếu cần lưu "đóng băng" số liệu đã báo cáo:

`bc_kln_snapshot` *[Đề xuất kỹ thuật]*: `id, mau_bao_cao VARCHAR(10) [01..08], don_vi_bao_cao_id FK, ky_bao_cao_id FK→dm_ky_bao_cao, nam INT, thang TINYINT NULL, du_lieu_json JSONB` — lưu bản chốt số liệu đã gửi đi (phục vụ đối chiếu, không tính lại nếu dữ liệu gốc bị sửa sau khi đã báo cáo).

---

### D.3. MIỀN DINH DƯỠNG TRONG PHÒNG BỆNH

*Căn cứ: Điều 41–47 TT15; Mẫu 01–08 – Phụ lục III QĐ97*

#### D.3.1. `dd_doi_tuong_dinh_duong` — Sổ ghi nhận đối tượng mắc bệnh liên quan dinh dưỡng
*Mẫu 01 – Phụ lục III*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| nguoi_id | BIGINT | FK→nguoi, NN | |
| ngay_kham | DATE | NN | |
| noi_kham_id | BIGINT | FK→dm_don_vi | |
| chieu_cao_cm | DECIMAL(5,1) | | |
| can_nang_kg | DECIMAL(5,1) | | |
| tinh_trang_dinh_duong | VARCHAR(30) | NN | `binh_thuong`\|`nhe_can`\|`gay_com`\|`thap_coi`\|`thua_can`\|`beo_phi`\|`thieu_nang_luong_truong_dien` (người ≥19 tuổi) |
| dau_hieu_thieu_vi_chat | TEXT | | Da xanh, móng giòn, tóc khô, đổ mồ hôi trộm, ngủ không sâu... |
| chi_dinh | TEXT | | Chế độ ăn hoặc chuyển khám chuyên sâu |
| nam_theo_doi | INT | NN | |

#### D.3.2. `dd_tre_sdd_cap_tinh` — Sổ quản lý trẻ 6–59 tháng suy dinh dưỡng cấp tính
*Mẫu 02 – Phụ lục III*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| nguoi_id | BIGINT | FK→nguoi, NN | Trẻ 6–59 tháng |
| thang_nam_theo_doi | VARCHAR(7) | NN | yyyy-mm |
| ngay_kham | DATE | | |
| noi_kham_id | BIGINT | FK→dm_don_vi | |
| chieu_cao_cm | DECIMAL(5,1) | | |
| can_nang_kg | DECIMAL(5,1) | | |
| chu_vi_vong_canh_tay_cm | DECIMAL(4,1) | | |
| dau_hieu_phu | BOOLEAN | | |
| muc_do_sdd_cap_tinh | VARCHAR(20) | | `vua`\|`nang`\|`co_bien_chung` |
| loai_hinh_quan_ly | VARCHAR(30) | | `dieu_tri_ngoai_tru`\|`dieu_tri_du_phong`\|`chuyen_noi_tru`\|`xuat_khoi_chuong_trinh` |

#### D.3.3. Báo cáo dinh dưỡng định kỳ
Mẫu 03–06 (báo cáo 6 tháng/năm cấp xã & tỉnh: tình trạng dinh dưỡng trẻ 0–59 tháng, người ≥5 tuổi theo 3 nhóm tuổi 5-18/19-59/≥60) và Mẫu 07–08 (điều tra định kỳ hằng năm/5 năm) là **báo cáo tổng hợp theo chỉ tiêu** → mô hình hoá theo Phần E (`bc_chi_tieu_thong_ke`) với danh mục chỉ tiêu `dm_chi_tieu` domain = `dinh_duong` (vd: tỷ lệ suy dinh dưỡng thấp còi/nhẹ cân/gầy còm/thừa cân/béo phì theo nhóm tuổi/giới/khu vực, tỷ lệ bú sớm, bú mẹ hoàn toàn, ăn bổ sung hợp lý, vi chất...).

---

### D.4. MIỀN DỰ PHÒNG THƯƠNG TÍCH TẠI CỘNG ĐỒNG

*Căn cứ: Điều 48–53 TT15; Mẫu 01–13 – Phụ lục IV QĐ97*

#### D.4.1. `tt_nguoi_bi_thuong_tich` — Người bị thương tích (gộp Mẫu 01 TYT xã + Mẫu 02 CSKCB)
*Căn cứ: Điều 49*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| nguoi_id | BIGINT | FK→nguoi, NN | |
| don_vi_ghi_nhan_id | BIGINT | FK→dm_don_vi, NN | TYT xã hoặc CSKCB |
| ngay_den_kham | DATETIME | NN | |
| thoi_gian_bi_thuong_tich | DATETIME | | |
| dia_diem_xay_ra_id | BIGINT | FK→dm_dia_diem_xay_ra_thuong_tich, NN | Hộ gia đình / Cơ sở giáo dục / Khu vực công cộng |
| bo_phan_bi_thuong_id | BIGINT | FK→dm_bo_phan_bi_thuong, NN | |
| nguyen_nhan_id | BIGINT | FK→dm_nguyen_nhan_thuong_tich, NN | 1 trong 13 nguyên nhân |
| muc_do_id | BIGINT | FK→dm_muc_do_thuong_tich, NN | Nhẹ/Trung bình/Nặng |
| hinh_thuc_vao_vien | VARCHAR(20) | | (chỉ CSKCB) `cap_cuu`\|`kham_thuong`\|`chuyen_cap_chuyen_mon` |
| ket_qua_dieu_tri | VARCHAR(20) | NN | `ra_vien`\|`chuyen_cap_chuyen_mon`\|`nang_xin_ve` (chỉ CSKCB có thêm "nặng xin về") |

#### D.4.2. `tt_nguoi_tu_vong_thuong_tich`
*Mẫu 09 PL IV; căn cứ Điều 50*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| nguoi_id | BIGINT | FK→nguoi, NN | |
| don_vi_ghi_nhan_id | BIGINT | FK→dm_don_vi, NN | |
| nguyen_nhan_id | BIGINT | FK→dm_nguyen_nhan_thuong_tich, NN | |
| noi_tu_vong | VARCHAR(20) | NN | `co_so_y_te`\|`cong_dong` |
| ngay_tu_vong | DATE | NN | |
| kham_dieu_tri_truoc_tu_vong_30_ngay | BOOLEAN | | Điều 48.1b: người tử vong do thương tích đến khám trong vòng 30 ngày trước khi tử vong |

#### D.4.3. `tt_yeu_to_nguy_co` — Giám sát yếu tố nguy cơ (gộp Mẫu 03 hộ gia đình, 04 khu vực công cộng, 05 cơ sở giáo dục)
*Căn cứ: Điều 51*

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| loai_dia_diem | VARCHAR(20) | NN | `ho_gia_dinh`\|`khu_vuc_cong_cong`\|`co_so_giao_duc` |
| ten_dia_diem | VARCHAR(300) | | Tên chủ hộ / tên khu vực / tên cơ sở giáo dục |
| dia_chi | VARCHAR(500) | NN | |
| don_vi_giam_sat_id | BIGINT | FK→dm_don_vi, NN | |
| ngay_giam_sat | DATE | NN | |
| nhom_yeu_to | VARCHAR(20) | NN | `moi_truong`\|`hanh_vi`\|`khac` |
| noi_dung | VARCHAR(500) | NN | Có thể tham chiếu `dm_yeu_to_nguy_co_thuong_tich_mau` hoặc nhập tự do |
| ket_qua | VARCHAR(10) | | `co`\|`khong` |
| da_huong_dan_can_thiep | BOOLEAN | | |

`tt_yeu_to_nguy_co_nhan_xet` (1-1 với phiếu giám sát — mục "Nhận xét" cuối mỗi mẫu): `giam_sat_id FK, tong_so_yeu_to_phat_hien INT, so_moi_truong INT, so_hanh_vi INT, so_khac INT, so_da_can_thiep_moi_truong INT, so_da_can_thiep_hanh_vi INT, so_da_can_thiep_khac INT, loai_hinh_nguy_co_cao_nhat VARCHAR(100)`

#### D.4.4. Báo cáo tổng hợp thương tích
Mẫu 08 (TYT xã), 10 (CSKCB), 11 (TTKSBT tỉnh), 12 (tử vong cấp tỉnh), 13 (Viện SKNN&MT toàn quốc) đều là **tổng hợp có cấu trúc cố định** (phân tổ theo nhóm tuổi × giới × nghề nghiệp × địa điểm × bộ phận × nguyên nhân × mức độ × kết quả điều trị) trực tiếp từ `tt_nguoi_bi_thuong_tich` / `tt_nguoi_tu_vong_thuong_tich` / `tt_yeu_to_nguy_co` → nên triển khai bằng **VIEW/aggregation query**, không tạo bảng lưu trùng lặp (trừ khi cần snapshot lịch sử báo cáo — xem `bc_*_snapshot` Phần E).

---

## PHẦN E. MÔ HÌNH CHỈ TIÊU THỐNG KÊ & BÁO CÁO TỔNG HỢP (khuyến nghị)

Quan sát: hơn 20 "Mẫu báo cáo" tổng hợp trong QĐ 97 (Mẫu 02, 04–08 PL II; Mẫu 03–08 PL III; Mẫu 08, 10–13 PL IV) có cùng bản chất: **đếm/tỷ lệ theo chỉ tiêu, phân tổ theo đơn vị báo cáo + kỳ báo cáo + (giới tính/nhóm tuổi/khu vực...)**. Thay vì tạo ~25 bảng gần giống hệt nhau, đề xuất mô hình fact-table dùng chung:

### E.1. `dm_chi_tieu` — Danh mục chỉ tiêu báo cáo
*[Đề xuất kỹ thuật, ánh xạ 1-1 tới từng dòng trong các Mẫu báo cáo]*

| Trường | Kiểu | Mô tả |
|---|---|---|
| id | BIGINT | PK |
| ma_chi_tieu | VARCHAR(30) | UQ, vd `TT_5.3_DUOI_NUOC`, `KLN_I.1_THA_KHAM_12T` |
| ten_chi_tieu | VARCHAR(500) | Nguyên văn dòng chỉ tiêu trong mẫu, vd "Số bệnh nhân đến khám và lấy thuốc ít nhất 1 lần trong 12 tháng qua" |
| mau_bao_cao | VARCHAR(20) | Vd `PL_II_M02`, `PL_IV_M08` |
| linh_vuc | VARCHAR(20) | `benh_truyen_nhiem`\|`khong_lay_nhiem`\|`roi_loan_tam_than`\|`dinh_duong`\|`thuong_tich` |
| don_vi_tinh | VARCHAR(20) | `nguoi`\|`%`\|`ca`\|`lan`... |
| cong_thuc | TEXT | Nếu là tỷ lệ (vd "số lượng / tổng số cân đo × 100%") |

### E.2. `bc_chi_tieu_thong_ke` — Bảng dữ kiện báo cáo (fact table)

| Trường | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | BIGINT | PK | |
| chi_tieu_id | BIGINT | FK→dm_chi_tieu, NN | |
| don_vi_bao_cao_id | BIGINT | FK→dm_don_vi, NN | |
| ky_bao_cao | VARCHAR(10) | NN | `thang`\|`6thang`\|`nam`\|`5nam`\|`dot_xuat` |
| nam | INT | NN | |
| thang | TINYINT | | NULL nếu kỳ ≠ tháng |
| phan_to_gioi_tinh | VARCHAR(10) | | `nam`\|`nu`\|`chung` |
| phan_to_nhom_tuoi | VARCHAR(20) | | Vd `0-4`, `5-15`, `16-19`, `20-60`, `>60` (thương tích) hoặc `0-59thang`, `5-18`, `19-59`, `>=60` (dinh dưỡng) |
| phan_to_khac | VARCHAR(100) | | Vd tuyến (xã/tỉnh/TW/tư nhân), khu vực (thành thị/nông thôn), mức độ (vừa/nặng) |
| gia_tri_so_luong | DECIMAL(18,2) | | |
| gia_tri_ty_le | DECIMAL(9,4) | | |
| nguon_tinh_toan | VARCHAR(20) | NN | `tu_dong_tu_du_lieu_tac_nghiep`\|`nhap_thu_cong` |
| ngay_chot_so_lieu | DATETIME | NN | |
| trang_thai_gui | VARCHAR(20) | NN | `nhap`\|`da_gui`\|`da_duyet`\|`tra_lai` |

→ Ưu điểm: (1) thêm chỉ tiêu mới (khi Cục Phòng bệnh cập nhật mẫu) chỉ cần thêm dòng `dm_chi_tieu`, không sửa schema; (2) truy vấn chéo mảng/kỳ dễ dàng; (3) vẫn tra ngược được đúng ô trong đúng Mẫu nào của QĐ 97 qua `mau_bao_cao`.

### E.3. Phương án thay thế (nếu tổ chức muốn bám sát 1-1 từng mẫu giấy)
Có thể giữ 1 bảng vật lý riêng cho mỗi Mẫu (vd `bc_pl2_mau02`, `bc_pl4_mau08`...) với cột đúng như trong mẫu — đơn giản hơn để đối chiếu khi thanh/kiểm tra nhưng khó mở rộng khi mẫu thay đổi. Lựa chọn theo năng lực đội ngũ vận hành.

---

## PHẦN F. MA TRẬN LUỒNG BÁO CÁO THEO CẤP

| Miền | Đơn vị gửi | Đơn vị nhận | Kỳ hạn | Căn cứ |
|---|---|---|---|---|
| Truyền nhiễm – ca bệnh | TYT xã/CSKCB/CS xét nghiệm | Hệ thống TT giám sát (trực tuyến) | 24h (nhóm ĐBNH), 48h (nhóm NH), tuần (nhóm còn lại) | Điều 10.1–2, Danh mục 01 PL I |
| Truyền nhiễm – tổng hợp | TTKSBT tỉnh | CQ chuyên môn y tế tỉnh + 1 trong 6 Viện VSDT/Pasteur/SR-KST-CT theo địa bàn | Liên tục/định kỳ theo hướng dẫn CPB | Điều 10.3 |
| Truyền nhiễm – Viện vùng | 6 Viện khu vực | Viện VSDT TW / Viện SR-KST-CT TW | | Điều 10.4 |
| Truyền nhiễm – TW | Viện VSDT TW, SR-KST-CT TW, BV Phổi TW | Cục Phòng bệnh (+ Cục QLKCB cho bệnh lao) | | Điều 10.5–6 |
| Truyền nhiễm – dịch/ổ dịch | TYT xã | Chủ tịch UBND xã, CQ chuyên môn y tế tỉnh, TTKSBT tỉnh, lực lượng chuyên trách | 24h kể từ khi xác định có/hết dịch; báo cáo ổ dịch hằng ngày tới khi kết thúc | Điều 26.1 |
| Không lây nhiễm & RLTT | CSKCB/cơ sở bảo trợ XH | TTKSBT tỉnh | 5 ngày làm việc sau kỳ báo cáo | Điều 33.1, 40.1 |
| " | TYT xã | TTKSBT tỉnh | 10 ngày làm việc | Điều 33.2, 40.2 |
| " | TTKSBT tỉnh | CQ chuyên môn y tế tỉnh + Viện phụ trách | 15 ngày làm việc (phản hồi TYT xã) | Điều 33.3, 40.3 |
| " | Viện phụ trách | Cục Phòng bệnh | 20 ngày làm việc | Điều 33.4, 40.4 |
| " | Đơn vị đầu mối điều tra định kỳ | Cấp trên | 5 ngày làm việc sau khi có kết quả | Điều 33.5, 40.5 |
| Dinh dưỡng – thường xuyên | TYT xã | TTKSBT tỉnh | 10 ngày làm việc | Điều 46.2a |
| " | TTKSBT tỉnh | CQ chuyên môn y tế tỉnh + Viện Dinh dưỡng/Pasteur Nha Trang/VSDT Tây Nguyên/YTCC TP.HCM | 20 ngày làm việc | Điều 46.2b |
| " | Viện Dinh dưỡng | Cục Phòng bệnh | 30 ngày làm việc | Điều 46.2c |
| Dinh dưỡng – điều tra hằng năm (trẻ <5 tuổi) | TTKSBT tỉnh | CQ chuyên môn y tế tỉnh + Viện Dinh dưỡng | 15 ngày làm việc | Điều 47.3a |
| " | Viện Dinh dưỡng | Cục Phòng bệnh | 60 ngày làm việc | Điều 47.3a |
| Dinh dưỡng – điều tra 5 năm | Viện Dinh dưỡng | Cục Phòng bệnh | 15 ngày kể từ khi công bố kết quả | Điều 47.3b |
| Thương tích | Cơ sở giáo dục | TYT xã | 5 ngày làm việc (định kỳ 6 tháng/năm) | Điều 53.1 |
| " | TYT xã | TTKSBT tỉnh | 10 ngày làm việc | Điều 53.2 |
| " | CSKCB | TTKSBT tỉnh | 5 ngày làm việc | Điều 53.3 |
| " | TTKSBT tỉnh | CQ chuyên môn y tế tỉnh + Viện SKNN&MT/YTCC TP.HCM/Pasteur Nha Trang/VSDT Tây Nguyên | 20 ngày làm việc | Điều 53.4 |
| " | Viện SKNN&MT | Cục Phòng bệnh | 30 ngày làm việc | Điều 53.5 |

→ Bảng hỗ trợ: `bc_luong_bao_cao` *[Đề xuất kỹ thuật]*: `id, don_vi_gui_id FK, don_vi_nhan_id FK, linh_vuc, ky_bao_cao_id FK, han_gui DATE, ngay_gui_thuc_te DATETIME, trang_thai [dung_han|tre_han|chua_gui]` — dùng để giám sát tuân thủ thời hạn báo cáo và tính chỉ tiêu "tỷ lệ đơn vị gửi đúng hạn" (xuất hiện tại Mẫu 13 PL IV mục I.1).

---

## PHẦN G. RÀNG BUỘC NGHIỆP VỤ QUAN TRỌNG (business rules cần triển khai ở tầng ứng dụng/CSDL)

1. **Phân loại nhóm bệnh truyền nhiễm** (Điều 14, 15, Phụ lục I TT15): `tong_diem = diem_1+diem_2+diem_3+diem_4`; `nhom = 'A' nếu tong_diem>=10 OR co_dac_biet_nguy_hiem_moi_phat_sinh; 'B' nếu 7<=tong_diem<=9; 'C' nếu tong_diem<7`. Nên cài đặt bằng trigger/computed column, không cho nhập tay `nhom_phan_loai` trực tiếp.
2. **Xác định có dịch cấp xã** (Điều 16.1):
   - Nhóm A: theo hướng dẫn chuyên môn riêng từng bệnh (không công thức chung — cần bảng `dm_tieu_chi_dich_nhom_a` lưu ngưỡng riêng do Cục Phòng bệnh ban hành theo từng bệnh, hiện chưa có trong TT15/QĐ97, cần bổ sung khi có hướng dẫn chuyên môn).
   - Nhóm B/C lưu hành: `so_mac_cong_don_thang > trung_binh_5nam_cung_ky + 2×do_lech_chuan`.
   - Nhóm B/C không lưu hành: `so_mac_cong_don_thang >= 5 AND co_lien_quan_dich_te`.
3. **Cảnh báo dịch cấp xã** (Điều 22.1) — ngưỡng theo tuần, hệ số 1–2 lần độ lệch chuẩn (nhẹ hơn ngưỡng "có dịch" theo tháng ở mục 2), nhóm B/C không lưu hành ngưỡng 3 ca liên quan dịch tễ (thấp hơn ngưỡng "có dịch" là 5 ca).
4. **Cấp độ phòng thủ dân sự** (Điều 17–19): điều kiện lồng nhau theo cấp hành chính (cấp 1 → cấp 2 → cấp 3), mỗi cấp cần kiểm tra đồng thời 3 điều kiện (có dịch đạt ngưỡng, năng lực địa phương không đáp ứng, cấp trên còn khả năng ứng phó) — nên triển khai bằng stored procedure/rule engine, có nhật ký `btn_cap_do_phong_thu_dan_su` lưu vết diễn biến ban bố/bãi bỏ.
5. **Thời hạn báo cáo tự động cảnh báo trễ hạn**: so khớp `ngay_gui_thuc_te` với `han_gui` tính từ `ngay_ket_thuc_ky_bao_cao + so_ngay_lam_viec_quy_dinh` (bảng F).
6. **Toàn vẹn tham chiếu ICD-10**: khi nhập `btn_truong_hop_benh`/`kln_nguoi_benh`/tử vong, mã ICD-10 phải thuộc danh mục đã khai báo trong `dm_*_icd10` tương ứng — đúng theo ghi chú Danh mục 01 PL I: *"đối với bệnh phải báo cáo nhưng chưa có mã ICD-10 theo TT06/2026/TT-BYT, vẫn phải báo cáo trực tiếp"* → cho phép `ma_icd10` NULL nhưng bắt buộc `benh_id` khớp danh mục.
7. **Không trùng lặp báo cáo theo người** (Điều 33 nguyên tắc ngầm định + hướng dẫn Mẫu 06 PL II): thống kê theo địa bàn dân cư (xã nơi cư trú), 1 người có nhiều lượt khám trong kỳ → chỉ lấy lần khám sau cùng.

---

## PHẦN H. PHÂN QUYỀN & AN TOÀN DỮ LIỆU (Điều 3.3 TT15)

- `ht_nguoi_dung (id, ho_ten, ma_dinh_danh, don_vi_id FK, ...)`
- `ht_vai_tro (id, ten_vai_tro)` — vd: Nhân viên TYT xã, Cán bộ TTKSBT tỉnh, Cán bộ Viện, Cán bộ Cục Phòng bệnh, Quản trị hệ thống.
- `ht_phan_quyen (vai_tro_id, chuc_nang, muc_do [xem|nhap|sua|duyet|xuat])` — phạm vi dữ liệu giới hạn theo `don_vi_id` và cấp quản lý (đơn vị con trong cây `dm_don_vi`).
- `ht_nhat_ky_truy_cap (id, nguoi_dung_id, hanh_dong, doi_tuong, thoi_gian, dia_chi_ip)` — audit log phục vụ yêu cầu an toàn/an ninh mạng và bảo vệ dữ liệu cá nhân.
- Dữ liệu định danh cá nhân (`nguoi.so_dinh_danh_ca_nhan`, họ tên, địa chỉ) cần mã hoá tại chỗ (encryption at rest) và kiểm soát truy cập theo nguyên tắc "biết trong phạm vi cần biết" — chỉ đơn vị quản lý địa bàn hoặc cấp trên trực tiếp mới xem được thông tin định danh đầy đủ; báo cáo tổng hợp gửi lên cấp cao hơn nên ở dạng số liệu đã ẩn danh (phù hợp với việc các Mẫu báo cáo cấp tỉnh/TW trong QĐ97 đều là *số liệu tổng hợp*, không có cột định danh cá nhân).

---

## PHẦN I. TÓM TẮT DANH SÁCH BẢNG

| Nhóm | Số bảng chính | Ghi chú |
|---|---|---|
| Danh mục dùng chung (`dm_*`) | 9 bảng lõi + ~7 bảng nhỏ | Phần C |
| Dùng chung person (`nguoi`) | 1 | Phần D.0 |
| Bệnh truyền nhiễm (`btn_*`) | 10 | Phần D.1 |
| Không lây nhiễm/RLTT (`kln_*`) | 8 | Phần D.2 |
| Dinh dưỡng (`dd_*`) | 2 (+ báo cáo dùng chung) | Phần D.3 |
| Thương tích (`tt_*`) | 4 (+ báo cáo dùng chung) | Phần D.4 |
| Báo cáo/thống kê (`bc_*`) | 3 | Phần E, F |
| Hệ thống (`ht_*`) | 4 | Phần H |

**Tổng cộng khoảng 45–50 bảng vật lý** (chưa kể bảng con lưu chi tiết theo dòng/theo tháng), thay vì >60 bảng nếu ánh xạ máy móc 1-1 từng Mẫu biểu trong QĐ 97 — nhờ (a) gộp person dùng chung, (b) gộp các "sổ theo dõi theo tháng" cùng cấu trúc, (c) mô hình hoá báo cáo tổng hợp bằng fact-table chỉ tiêu thay vì bảng riêng từng mẫu.

---

## PHỤ LỤC: BẢNG ĐỐI CHIẾU CĂN CỨ PHÁP LÝ ↔ BẢNG DỮ LIỆU

| Điều/Mẫu | Bảng CSDL tương ứng |
|---|---|
| Điều 5 | btn_doi_tuong_giam_sat |
| Điều 6–9 | dm_loai_hinh_giam_sat (thuộc tính phân loại trên các bảng nghiệp vụ) |
| Mẫu 01 PL I | btn_truong_hop_benh |
| Mẫu 02, 03 PL I | btn_o_dich, btn_o_dich_so_lieu_ngay, btn_o_dich_tong_hop |
| Mẫu 04, 05 PL I | btn_bao_cao_dich_benh_chi_tiet |
| Mẫu 01, 02 PL II (TT15) | btn_bao_cao_dich_benh |
| Điều 12–13 | btn_khai_bao_ca_nhan |
| Điều 14–15, PL I (TT15) | dm_benh_truyen_nhiem |
| Điều 16 | quy tắc G.2 + btn_o_dich.trang_thai |
| Điều 17–20 | btn_cap_do_phong_thu_dan_su |
| Điều 21 | btn_danh_gia_nguy_co |
| Điều 22 | btn_canh_bao_dich_benh |
| Điều 23 | btn_dieu_tra_o_dich |
| Điều 24 | btn_bien_phap_xu_ly_o_dich |
| Danh mục 01 PL I | dm_benh_truyen_nhiem, dm_benh_truyen_nhiem_icd10 |
| Mục I PL II (QĐ97) | dm_benh_khong_lay_nhiem, dm_roi_loan_tam_than |
| Mẫu sổ 01A–06 PL II | kln_nguoi_benh, kln_lan_kham_*, kln_nguoi_nguy_co_* |
| Mẫu 01–08 PL II | bc_chi_tieu_thong_ke (linh_vuc=khong_lay_nhiem/roi_loan_tam_than) |
| Mẫu 01, 02 PL III | dd_doi_tuong_dinh_duong, dd_tre_sdd_cap_tinh |
| Mẫu 03–08 PL III | bc_chi_tieu_thong_ke (linh_vuc=dinh_duong) |
| Mẫu 01, 02 PL IV | tt_nguoi_bi_thuong_tich |
| Mẫu 03, 04, 05 PL IV | tt_yeu_to_nguy_co |
| Mẫu 06, 07 PL IV | dm_yeu_to_nguy_co_thuong_tich_mau |
| Mẫu 09 PL IV | tt_nguoi_tu_vong_thuong_tich |
| Mẫu 08, 10–13 PL IV | bc_chi_tieu_thong_ke (linh_vuc=thuong_tich) |
| Điều 3.3 (an toàn dữ liệu) | ht_nguoi_dung, ht_vai_tro, ht_phan_quyen, ht_nhat_ky_truy_cap |
