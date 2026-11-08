# 🌌 Tử Vi Đẩu Số Thiên Kỷ (Tu Vi Thien Ky)

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Web%20%7C%20CLI-blue.svg)](https://github.com)
[![Methodology](https://img.shields.io/badge/Methodology-Master%20Ni%20Hai--sha-rose.svg)](docs/THIEN_KY_HEMING_GUIDE.md)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Client--Side-emerald.svg)](#bảo-mật-quyền-riêng-tư-privacy-first)

> **Hệ thống An Sao Tử Vi Đẩu Số, Khảm Bàn Hợp Tuổi (Heming) & Phong Thủy Dương Trạch Cửu Cung** theo chân truyền của **Đại Sư Nghê Hải Hạ (倪海厦)** kết hợp công cụ trích xuất dữ liệu 56.6 GB (`Renhuai123/ziwei-doushu` Release `v4.0-13d`).

---

## ✨ Điểm Nổi Bật (Key Features)

1. **Mệnh Bàn 12 Cung Tương Tác Trực Quan**:
   - Giao diện 4x4 truyền thống với Trung Cung (Thiên Bàn) và 12 cung Địa Chi.
   - **Tia Chiếu Động SVG**: Tự động vẽ đường Tam Phương Tứ Chính (Tam Hợp, Đối Cung Xung Chiếu, Giáp Cung) khi nhấp chuột vào từng cung.
   - Tự động an sao 14 chính tinh, Tứ Hóa tiên thiên, phụ tinh cát/hung, Đại Vận 10 năm, Tiểu Hạn và Vòng Trường Sinh.
   - Tích hợp 99+ **Khẩu Quyết Chân Truyền** của Đại sư Nghê Hải Hạ từ bộ băng giảng *《Thiên Kỷ》*.
   - Hỗ trợ đổi năm xem Hạn (Lưu Niên 2024–2035) tức thì.

2. **Hiệu Chỉnh Chân Thái Dương Thời (True Solar Time)**:
   - Tích hợp sẵn tọa độ kinh độ của **63 tỉnh thành Việt Nam**.
   - Tự động tính độ lệch kinh độ so với kinh tuyến chuẩn GMT+7 ($105.0^\circ\text{E}$) và phương trình thời gian (Equation of Time - EoT).

3. **Thuật Khảm Bàn Tử Vi Đôi Lứa & Đối Tác (Heming Engine)**:
   - Chấm điểm tương hợp theo thang điểm **100 điểm minh bạch** qua 4 trụ cột:
     - 🌟 Ngũ Hành Bản Mệnh (25 điểm)
     - ☯️ Địa Chi & Tam Hợp Cục (25 điểm)
     - 🏛️ Cung Vị Tương Phối (25 điểm)
     - ⚡ Khí Vận Tứ Hóa Phi Cung (25 điểm)
   - 3 chế độ chuyên biệt: *Hôn Nhân & Tình Duyên*, *Cha Mẹ & Con Cái*, *Hợp Tác Làm Ăn*.
   - Khuyến nghị phong thủy Dương Trạch chuyển hóa điểm xung khắc.

4. **Đồ Hình Phong Thủy Dương Trạch Cửu Cung (Địa Kỷ)**:
   - Phân bổ 9 cung vị phòng ngủ theo quẻ Bát Quái (Càn, Khảm, Cấn, Chấn, Tốn, Ly, Khôn, Đoài, Trung Cung).
   - Tự động gán vị trí tối ưu cho từng thành viên trong gia đình theo nguyên lý *《Địa Thiên Thái》*.

5. **CLI Trích Xuất Dữ Liệu 56.6 GB (`scripts/tuvi_cli.py`)**:
   - Kết nối trực tiếp tới kho dữ liệu mở 56.6 GB `v4.0-13d`.
   - Streaming tải gói năm sinh `year-YYYY.jsonl.zst` (khoảng 2 MB) và giải nén siêu tốc bằng `zstandard`.
   - Tự động biên dịch 13 chiều kích luận giải chuyên sâu sang Tiếng Việt.

---

## 🔒 Bảo Mật Quyền Riêng Tư (Privacy First)

- **100% Client-Side**: Toàn bộ thuật toán an sao, lịch Âm-Dương và chấm điểm Khảm Bàn chạy hoàn toàn trong trình duyệt web của bạn.
- **Không gửi dữ liệu ra ngoài**: Danh sách hồ sơ cá nhân và gia đình được lưu trữ an toàn trong `localStorage` của trình duyệt của bạn. Bạn có thể xuất và nhập file JSON dự phòng bất cứ lúc nào.
- Kho mã nguồn mở này hoàn toàn **không chứa bất kỳ dữ liệu cá nhân thực tế nào** của bất kỳ ai.

---

## 🚀 Hướng Dẫn Sử Dụng (Quick Start)

### Cách 1: Chạy trực tiếp trên Web (Không cần cài đặt)

Chỉ cần mở file `index.html` bằng bất kỳ trình duyệt nào (Chrome, Edge, Firefox, Safari) hoặc kích hoạt **GitHub Pages**:
1. Fork hoặc clone repo này.
2. Vào **Settings** > **Pages** trên GitHub repository của bạn.
3. Chọn nhánh `main` và thư mục `/ (root)` rồi bấm **Save**.
4. Trang web sẽ trực tiếp hoạt động tại `https://<username>.github.io/<repo-name>/`.

---

### Cách 2: Sử dụng công cụ dòng lệnh (CLI Toolkit)

#### 1. Cài đặt thư viện phụ thuộc:
```bash
pip install zstandard
```

#### 2. Chạy lệnh trích xuất 13 chiều từ kho dữ liệu 56.6 GB:
```bash
python scripts/tuvi_cli.py --name "Nguyễn Văn A" --gender male --day 15 --month 8 --year 1990 --hour-idx 8 --province "Hà Nội"
```

Hoặc tính giờ sinh chính xác theo đồng hồ:
```bash
python scripts/tuvi_cli.py --name "Trần Thị B" --gender female --day 20 --month 10 --year 1995 --clock-time "16:30" --province "TP.HCM"
```

Dữ liệu kết quả sẽ được lưu vào thư mục `output/` dưới định dạng JSON song ngữ chuẩn hóa.

---

## 📁 Cấu Trúc Thư Mục (Project Structure)

```
tuvi-thien-ky/
├── index.html                   # Web App độc lập, hỗ trợ GitHub Pages
├── LICENSE                      # Giấy phép nguồn mở MIT
├── README.md                    # Tài liệu hướng dẫn sử dụng
├── .gitignore                   # Chặn file rác, dữ liệu lớn và file cá nhân
├── assets/                      # Động cơ JS lõi & bộ nhớ dịch thuật
│   ├── lunarCalendar-uRN2mj9t.js
│   ├── tuviEngine-CphnIt2k.js
│   ├── niHaiShaQuotes-DtbAK7ef.js
│   └── vi_translation_memory.json
├── scripts/
│   └── tuvi_cli.py             # CLI trích xuất & giải mã kho dữ liệu 56.6 GB
├── docs/
│   ├── ARCHITECTURE.md          # Kiến trúc hệ thống & công thức toán học
│   └── THIEN_KY_HEMING_GUIDE.md # Cẩm nang Khảm Bàn & Phong Thủy Nghê Hải Hạ
└── sample_data/
    └── sample_profiles.json     # Dữ liệu mẫu minh họa
```

---

## 📜 Tài Liệu Tham Khảo & Lời Cảm Ơn (Credits)

- **Đại Sư Nghê Hải Hạ (倪海厦)**: Tác giả bộ sách và bài giảng kinh điển *《Thiên Kỷ》*, *《Địa Kỷ》*, *《Nhân Gian Đạo》*.
- **Dự án mã nguồn mở Upstream**:
  - Repo dữ liệu 56.6 GB: [`Renhuai123/ziwei-doushu`](https://github.com/Renhuai123/ziwei-doushu)
  - Corpus luận giải: [`Renhuai123/nihai-tianji-corpus`](https://github.com/Renhuai123/nihai-tianji-corpus)
- Thuật toán Lịch Âm Việt Nam của Hồ Ngọc Đức.

---

## ⚖️ Tuyên Bố Miễn Trừ Trách Nhiệm (Disclaimer)

Ứng dụng này được phát triển cho mục đích học thuật, nghiên cứu văn hóa truyền thống Á Đông và chiêm nghiệm triết lý sống. Thuật số là công cụ để hiểu mình, thuận theo quy luật tự nhiên và hướng thiện, không mang tính mê tín dị đoan hay định đoạt số phận tuyệt đối.
