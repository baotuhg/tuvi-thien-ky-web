# Kiến Trúc Hệ Thống Tử Vi Đẩu Số Thiên Kỷ

Tài liệu mô tả chi tiết kiến trúc kỹ thuật của hệ thống **Tử Vi Đẩu Số Thiên Kỷ**, bao gồm thuật toán tính Chân Thái Dương Thời, động cơ an sao 12 cung, thuật toán Khảm Bàn (Heming), và kết nối với bộ dữ liệu 56.6 GB `v4.0-13d`.

---

## 1. Tổng Quan Kiến Trúc (Architecture Overview)

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Layer                          │
│  - index.html (Responsive Tailwind CSS + Native Canvas/SVG) │
│  - LocalStorage Profile Management (Zero-Server Privacy)    │
│  - Interactive 4x4 Grid Board with Dynamic Ray Tracing      │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┼────────────────────────┐
       ▼                       ▼                        ▼
┌──────────────┐      ┌─────────────────┐     ┌──────────────────┐
│ Lịch Âm-Dương│      │  Động Cơ An Sao │     │ Khẩu Quyết Nghê Sư│
│   (Lunar)    │      │  (TuVi Engine)  │     │   (Ni Quotes)    │
└──────┬───────┘      └────────┬────────┘     └────────┬─────────┘
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Thuật Toán Khảm Bàn (Heming)                │
│  1. Ngũ Hành Cục Số (25đ)   2. Địa Chi & Tam Hợp Cục (25đ)   │
│  3. Cung Vị Tương Phối (25đ) 4. Tứ Hóa Phi Cung (25đ)       │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Dương Trạch Địa Kỷ (Cửu Cung)               │
│  - Phối hợp Quẻ Danh gia đình vào 9 phương vị phong thủy    │
│  - Vợ chồng Cung Càn (Tây Bắc) đắc quẻ Địa Thiên Thái       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Hiệu Chỉnh Chân Thái Dương Thời (True Solar Time)

Múi giờ chuẩn của Việt Nam là UTC+7, lấy kinh tuyến chuẩn là $\lambda_0 = 105.00^\circ\text{E}$. Giờ đồng hồ dân dụng chỉ phản ánh giờ trung bình của kinh tuyến 105°. Để an sao Tử Vi chính xác, bắt buộc phải tính giờ Mặt Trời thực tại vị trí sinh:

$$T_{\text{thực}} = T_{\text{đồng hồ}} + \Delta t_{\text{kinh độ}} + \Delta t_{\text{EoT}}$$

Trong đó:
1. **Độ lệch kinh độ:**
   $$\Delta t_{\text{kinh độ}} = (\lambda_{\text{nơi sinh}} - 105.0^\circ) \times 4 \text{ (phút)}$$
2. **Phương trình thời gian (Equation of Time - EoT):**
   $$B = \frac{360^\circ}{365} \times (N_{\text{ngày trong năm}} - 81)$$
   $$\Delta t_{\text{EoT}} = 9.87 \sin(2B) - 7.53 \cos(B) - 1.5 \sin(B) \text{ (phút)}$$

---

## 3. Động Cơ Khảm Bàn (Heming Compatibility Engine)

Khảm Bàn của Đại sư Nghê Hải Hạ đối chiếu 2 lá số qua 4 trục:

1. **Ngũ Hành Bản Mệnh (25 điểm):** Tương sinh (25đ), Tỷ hòa (21đ), Chế hóa/Khắc nhẹ (15đ).
2. **Địa Chi & Tam Hợp Cục (25 điểm):** Lục Hợp (25đ), Tam Hợp Cục (24đ), Bình hòa (19đ), Tứ Xung (14đ).
3. **Cung Vị Tương Phối (25 điểm):** Trùng khớp chính tinh đắc cách giữa Mệnh và Phu Thê/Quan Lộc/Điền Trạch (25đ), Bổ khuyết âm dương (20đ).
4. **Khí Vận Tứ Hóa Phi Cung (25 điểm):** Can tuổi phát sinh Hóa Lộc, Hóa Quyền, Hóa Khoa bay vào cung vị cốt lõi của nhau (22–25đ).

---

## 4. Dữ Liệu 56.6 GB (`v4.0-13d`) & CLI Extraction

Hệ thống cung cấp kịch bản Python `scripts/tuvi_cli.py` sử dụng thư viện `zstandard` để giải nén trực tiếp dạng streaming (không cần tải toàn bộ 56.6 GB mà chỉ tải gói nén `year-YYYY.jsonl.zst` khoảng 2 MB cho năm cần tra cứu).

Mỗi bản ghi chứa 13 chiều kích:
- `overview`: Tổng quan bản chất cốt lõi
- `personality`: Chiều sâu tư duy & tâm lý
- `career`: Định vị sự nghiệp & quan lộc
- `wealth`: Tài bạch & mô thức tích lũy
- `love`: Chân dung phối ngẫu & hôn nhân
- `spirit`: Phúc đức & nền tảng tinh thần
- `health`: Tật ách & Đông Y kinh lạc
- `home`: Điền trạch & bất động sản
- `family`: Huynh đệ & bằng hữu
- `friends`: Giao hữu & đội ngũ
- `move`: Thiên di & phát triển bên ngoài
- `children`: Tử tức & định hướng con cái
- `parents`: Phụ mẫu & gia phong nền tảng
