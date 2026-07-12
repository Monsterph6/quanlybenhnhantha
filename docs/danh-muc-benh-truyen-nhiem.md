# DANH MỤC BỆNH TRUYỀN NHIỄM BÁO CÁO THEO THỜI GIAN

**Nguồn:** Danh mục 01 – Phụ lục I, Quyết định số 97/QĐ-PB ngày 30/6/2026 của Cục trưởng Cục Phòng bệnh (thực hiện Thông tư 15/2026/TT-BYT).
**Mã ICD-10:** theo Thông tư 06/2026/TT-BYT.

Danh mục dùng để nạp vào bảng `dm_benh_truyen_nhiem` (trường `ky_han_bao_cao`) và `dm_benh_truyen_nhiem_icd10`. Dữ liệu nạp sẵn: xem `du-lieu-mau-benh-truyen-nhiem.csv` và `seed_dm_benh_truyen_nhiem.sql`.

> **Lưu ý phân biệt:** "24h / 48h / tuần" là **kỳ hạn báo cáo từng trường hợp bệnh** theo Danh mục 01 QĐ97 (theo mức độ nguy hiểm), **không phải** phân loại nhóm A/B/C. Nhóm A/B/C được xác định riêng theo điểm số 4 tiêu chí tại Điều 14–15 và Phụ lục I của Thông tư 15/2026/TT-BYT.

### Nhóm 1 — Báo cáo trong vòng 24 giờ (18 bệnh)

Các bệnh truyền nhiễm **đặc biệt nguy hiểm** phải báo cáo từng trường hợp bệnh ngay sau khi có chẩn đoán và trong vòng 24 giờ.

| STT | Tên bệnh | Mã ICD-10 |
|---|---|---|
| 1 | Bệnh bại liệt | A80 |
| 2 | Bệnh dịch hạch | A20 |
| 3 | Bệnh do vi rút cúm A(H5N1) | J09 |
| 4 | Bệnh do vi rút cúm A(H5N6) | J09 |
| 5 | Bệnh do vi rút cúm A(H7N9) | J09 |
| 6 | Bệnh do vi rút cúm A(H9N2) | J09 |
| 7 | Bệnh do vi rút Ebola (Bệnh sốt xuất huyết do vi rút Ebola) | A98.4 |
| 8 | Bệnh do vi rút Lassa (Bệnh sốt xuất huyết do vi rút Lassa) | A96.2 |
| 9 | Bệnh do vi rút Marburg (Bệnh sốt xuất huyết do vi rút Marburg) | A98.3 |
| 10 | Bệnh do vi rút Nipah | B33.8 |
| 11 | Bệnh nhiễm vi rút tây sông Nin | A92.3 |
| 12 | Bệnh sốt vàng | A95 |
| 13 | Hội chứng suy hô hấp cấp tính nặng (SARS) | U04 |
| 14 | Hội chứng viêm đường hô hấp vùng Trung Đông (MERS-CoV) | B34.2 |
| 15 | Bệnh truyền nhiễm đặc biệt nguy hiểm mới phát sinh, chưa rõ tác nhân gây bệnh | _(chưa có mã ICD-10)_ |
| 16 | Bệnh bạch hầu | A36 |
| 17 | Bệnh nhiễm trùng do não mô cầu | A39 |
| 18 | Bệnh sởi | B05 |

### Nhóm 2 — Báo cáo trong vòng 48 giờ (17 bệnh)

Các bệnh truyền nhiễm **nguy hiểm** phải báo cáo từng trường hợp bệnh trong vòng 48 giờ kể từ khi có chẩn đoán.

| STT | Tên bệnh | Mã ICD-10 |
|---|---|---|
| 1 | Bệnh COVID-19 | U07.1, U07.2 |
| 2 | Bệnh dại | A82 |
| 3 | Bệnh đậu mùa khỉ (Mpox) | B04 |
| 4 | Bệnh do nhiễm vi rút Chikungunya | A92.0 |
| 5 | Bệnh do vi rút Hanta | A98.5, B33.4 |
| 6 | Bệnh nhiễm vi rút Zika | A92.5, P35.4 |
| 7 | Bệnh ho gà | A37 |
| 8 | Bệnh liên cầu lợn ở người | A40.8, G00.2 |
| 9 | Bệnh rubella | B06, P35.0 |
| 10 | Bệnh sốt xuất huyết Dengue | A97 |
| 11 | Bệnh sốt rét | B50 - B54 |
| 12 | Bệnh tả | A00 |
| 13 | Bệnh tay - chân - miệng | B08.4 |
| 14 | Bệnh than | A22 |
| 15 | Bệnh uốn ván | A33 - A35 |
| 16 | Bệnh viêm gan vi rút A | B15 |
| 17 | Bệnh viêm não Nhật Bản | A83.0 |

### Nhóm 3 — Báo cáo hàng tuần (46 bệnh)

Các bệnh truyền nhiễm phải báo cáo từng trường hợp bệnh hàng tuần (07 ngày, từ 00h00 thứ Hai đến 24h00 Chủ nhật; báo cáo trước thứ Tư tuần kế tiếp).

| STT | Tên bệnh | Mã ICD-10 |
|---|---|---|
| 1 | Bệnh cúm | J10, J11 |
| 2 | Bệnh do Haemophilus influenzae | G00.0, A41.3, J14, J05.1, J20.1 |
| 3 | Bệnh do nhiễm Listeria | A32, P37.2 |
| 4 | Bệnh do nhiễm nocardia | A43 |
| 5 | Bệnh do phế cầu | J13, A40.3, G00.1, M00.1 |
| 6 | Bệnh do vi rút Adeno khác | A87.1, A85.1, A08.2, B34.0, J12.0 |
| 7 | Bệnh viêm kết mạc do vi rút Adeno | B30.0†, B30.1† |
| 8 | Bệnh do vi rút gây ra hội chứng suy giảm miễn dịch mắc phải ở người (HIV/AIDS) | B20-B24, Z20.6, Z21 |
| 9 | Bệnh do vi rút hợp bào hô hấp (RSV) | J12.1, J20.5, J21.0 |
| 10 | Bệnh do vi rút HPV (Human Papilloma Virus) ở người | B07, A63.0 |
| 11 | Bệnh lao | A15, A16 |
| 12 | Bệnh Legionnaire | A48.1, A48.2 |
| 13 | Bệnh leptospira | A27 |
| 14 | Bệnh quai bị | B26 |
| 15 | Bệnh thương hàn | A01 |
| 16 | Bệnh thủy đậu | B01 |
| 17 | Bệnh tiêu chảy do vi rút Rota | A08.0 |
| 18 | Bệnh viêm gan vi rút B | B16, B18.0, B18.1 |
| 19 | Bệnh viêm gan vi rút C | B17.1, B18.2 |
| 20 | Bệnh viêm gan vi rút D | B17.0 |
| 21 | Bệnh viêm gan vi rút E | B17.2 |
| 22 | Bệnh viêm não vi rút | A83 - A86, G04.8, G04.9 |
| 23 | Bệnh viêm phế quản cấp tính do vi rút Coxsackie | J20.3 |
| 24 | Bệnh melioidosis (Whitmore) | A24 |
| 25 | Ngộ độc botulinum | A05.1 |
| 26 | Bệnh nhiễm ấu trùng sán lợn | B69 |
| 27 | Bệnh đường ruột do nhiễm giardia | A07.1 |
| 28 | Bệnh nhiễm giun | B72 - B75, B76 - B81, B83 |
| 29 | Bệnh giun đũa chó mèo | B83.0 |
| 30 | Bệnh do nhiễm nấm Candida | B37, B20.4 |
| 31 | Bệnh do nhiễm Rickettsia | A75.0, A75.2, A77, A79 |
| 32 | Bệnh nhiễm sán dây | B68, B70, B71 |
| 33 | Bệnh nhiễm sán dây chó | B67 |
| 34 | Bệnh nhiễm sán lá gan | B66 |
| 35 | Bệnh nhiễm sán lá phổi | B66.4 |
| 36 | Bệnh nhiễm sán lá ruột | B66.5, B66.8 |
| 37 | Bệnh do trichomonas | A59 |
| 38 | Bệnh nhiễm vi rút đại bào | B20.2, B25, B27.1, P35.1 |
| 39 | Bệnh do nhiễm vi rút herpes | A60, B00, B02, P35.2 |
| 40 | Bệnh giang mai | A50 - A53, A65 |
| 41 | Bệnh lậu | A54 |
| 42 | Bệnh lỵ a-míp | A06 |
| 43 | Bệnh lỵ trực khuẩn | A03 |
| 44 | Bệnh mắt hột | A71 |
| 45 | Bệnh phong | A30 |
| 46 | Ngộ độc thực phẩm do Vibrio Parahaemolyticus | A05.3 |
