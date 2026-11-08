#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tu Vi Thien Ky CLI — An Sao & Trích Xuất Dữ Liệu 56.6 GB (Hệ Thống Nghê Hải Hạ)
Hỗ trợ tính Chân Thái Dương Thời, tải dữ liệu v4.0-13d, trích xuất 13 chiều luận giải và dịch sang Tiếng Việt.
"""

import argparse
import datetime
import json
import math
import os
import re
import sys
import unicodedata
import urllib.request

try:
    import zstandard as zstd
except ImportError:
    zstd = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CACHE_DIR = os.path.join(BASE_DIR, "cache_v4_13d")
DEFAULT_OUT_DIR = os.path.join(BASE_DIR, "output")

# Danh mục kinh độ 63 tỉnh thành Việt Nam (độ Đông)
VN_PROVINCES_LON = {
    "hà giang": 104.983, "ha giang": 104.983,
    "hà nội": 105.834, "ha noi": 105.834,
    "tp.hcm": 106.660, "hồ chí minh": 106.660, "sài gòn": 106.660,
    "đà nẵng": 108.202, "da nang": 108.202,
    "hải phòng": 106.688, "hai phong": 106.688,
    "cần thơ": 105.747, "can tho": 105.747,
    "tuyên quang": 105.218, "lào cai": 103.970, "cao bằng": 106.252,
    "yên bái": 104.871, "thái nguyên": 105.848, "phú thọ": 105.402,
    "vĩnh phúc": 105.605, "bắc ninh": 106.076, "bắc giang": 106.197,
    "quảng ninh": 107.073, "hải dương": 106.331, "hưng yên": 106.051,
    "thái bình": 106.336, "nam định": 106.162, "ninh bình": 105.975,
    "hà nam": 105.923, "thanh hóa": 105.776, "nghệ an": 105.681,
    "hà tĩnh": 105.906, "quảng bình": 106.623, "quảng trị": 107.100,
    "huế": 107.590, "thừa thiên huế": 107.590, "quảng nam": 108.338,
    "quảng ngãi": 108.800, "bình định": 109.219, "phú yên": 109.092,
    "khánh hòa": 109.196, "nha trang": 109.196, "ninh thuận": 108.988,
    "bình thuận": 108.100, "phan thiết": 108.100, "kon tum": 108.000,
    "gia lai": 108.000, "đắk lắk": 108.038, "đắk nông": 107.684,
    "lâm đồng": 108.458, "đà lạt": 108.458, "bình phước": 106.726,
    "tây ninh": 106.098, "bình dương": 106.650, "đồng nai": 106.840,
    "bà rịa - vũng tàu": 107.084, "long an": 106.413, "tiền giang": 106.363,
    "bến tre": 106.375, "trà vinh": 106.346, "vĩnh long": 105.972,
    "đồng tháp": 105.631, "an giang": 105.125, "kiên giang": 105.080,
    "hậu giang": 105.470, "sóc trăng": 105.974, "bạc liêu": 105.724,
    "cà mau": 105.150
}

CHI_NAMES = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CHI_RANGES = [
    "23:00 - 01:00", "01:00 - 03:00", "03:00 - 05:00", "05:00 - 07:00",
    "07:00 - 09:00", "09:00 - 11:00", "11:00 - 13:00", "13:00 - 15:00",
    "15:00 - 17:00", "17:00 - 19:00", "19:00 - 21:00", "21:00 - 23:00"
]


def slugify(text: str) -> str:
    text = text.replace("Đ", "D").replace("đ", "d")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").upper()
    return text or "PROFILE"


def calc_true_solar_time(year: int, month: int, day: int, hour: int, minute: int, lon: float = 105.0):
    """
    Tính Chân Thái Dương Thời (True Solar Time):
    - Múi giờ Việt Nam GMT+7 có kinh tuyến chuẩn 105° Đông.
    - Hiệu chỉnh kinh độ = (Kinh độ - 105) * 4 phút.
    - Hiệu chỉnh phương trình thời gian (Equation of Time - EoT).
    """
    dt_clock = datetime.datetime(year, month, day, hour, minute)
    day_of_year = dt_clock.timetuple().tm_yday
    B = math.radians((360.0 / 365.0) * (day_of_year - 81))
    eot_min = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    lon_offset_min = (lon - 105.0) * 4.0
    total_offset_min = lon_offset_min + eot_min
    dt_true = dt_clock + datetime.timedelta(minutes=total_offset_min)

    h = dt_true.hour + dt_true.minute / 60.0
    if h >= 23.0 or h < 1.0:
        hour_idx = 0
    else:
        hour_idx = int((h + 1.0) // 2)

    return {
        "clock_time": dt_clock.strftime("%H:%M"),
        "true_solar_time": dt_true.strftime("%H:%M:%S"),
        "longitude": lon,
        "lon_offset_min": round(lon_offset_min, 2),
        "eot_min": round(eot_min, 2),
        "total_offset_min": round(total_offset_min, 2),
        "hour_idx": hour_idx,
        "chi_name": CHI_NAMES[hour_idx],
        "chi_range": CHI_RANGES[hour_idx],
    }


def ensure_year_archive(year: int) -> str:
    """Tải và lưu trữ bộ nén năm sinh year-YYYY.jsonl.zst từ GitHub Release v4.0-13d."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    archive_path = os.path.join(CACHE_DIR, f"year-{year}.jsonl.zst")
    if os.path.exists(archive_path) and os.path.getsize(archive_path) > 100_000:
        return archive_path

    url = f"https://github.com/Renhuai123/ziwei-doushu/releases/download/v4.0-13d/year-{year}.jsonl.zst"
    print(f"[*] Đang tải dữ liệu năm {year} từ kho 56.6 GB: {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (TuVi-ThienKy-Engine)"})
    with urllib.request.urlopen(req, timeout=90) as resp, open(archive_path, "wb") as out_f:
        downloaded = 0
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            out_f.write(chunk)
            downloaded += len(chunk)
            sys.stdout.write(f"\r  -> Đã tải: {downloaded / 1024 / 1024:.2f} MB")
            sys.stdout.flush()
    print(f"\n[+] Đã lưu cache: {archive_path} ({os.path.getsize(archive_path):,} bytes)")
    return archive_path


def extract_record_from_zst(year: int, month: int, day: int, hour_idx: int, gender: str) -> dict:
    if zstd is None:
        raise RuntimeError("Vui lòng cài đặt thư viện 'zstandard': pip install zstandard")
    archive_path = ensure_year_archive(year)
    target_id = f"{year:04d}-{month:02d}-{day:02d}-{hour_idx}-{gender}"
    print(f"[*] Đang tìm kiếm bản ghi ID: {target_id} ...")

    dctx = zstd.ZstdDecompressor()
    with open(archive_path, "rb") as fh:
        with dctx.stream_reader(fh) as reader:
            buffer = b""
            while True:
                chunk = reader.read(131072)
                if not chunk:
                    break
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if target_id.encode("utf-8") in line:
                        rec = json.loads(line.decode("utf-8"))
                        if rec.get("id") == target_id:
                            return rec
    raise ValueError(f"Không tìm thấy bản ghi {target_id} trong {os.path.basename(archive_path)}")


def translate_cn_to_vi_fallback(text: str, tm: dict) -> str:
    """Biên dịch và chuẩn hóa luận giải sang Tiếng Việt."""
    lines = text.split("\n")
    out_lines = []

    replacements = [
        ("【核心本质】", "【Bản chất cốt lõi】"),
        ("【高维亮点】", "【Điểm sáng nổi bật】"),
        ("【痛点与蜕变】", "【Điểm nghẽn & Chuyển hóa】"),
        ("【倪师断语】", "【Quyết đoán của Đại sư Nghê Hải Hạ】"),
        ("【古籍印证】", "【Cổ tịch đối chứng】"),
        ("【大运节奏】", "【Nhịp điệu Đại vận】"),
        ("【身体重点关注】", "【Trọng điểm sức khỏe Đông Y】"),
        ("【健康管理铁律】", "【Nguyên tắc dưỡng sinh cốt lõi】"),
        ("【外伤与手术防范】", "【Phòng ngừa ngoại thương & tiểu phẫu】"),
        ("【伴侣画像】", "【Chân dung người phối ngẫu】"),
        ("【相处模式】", "【Mô thức tương tác】"),
        ("【破局之道】", "【Bí quyết hóa giải & bồi đắp】"),
        ("【置业特征】", "【Đặc trưng gây dựng cơ ngơi】"),
        ("【居住风水】", "【Phong thủy Dương Trạch nơi ở】"),
        ("【不动产避坑】", "【Lưu ý pháp lý Bất động sản】"),
        ("【手足情缘】", "【Tình cảm anh chị em】"),
        ("【合伙铁律】", "【Nguyên tắc hợp tác làm ăn】"),
        ("【人脉质量】", "【Chất lượng mạng lưới quan hệ】"),
        ("【御下之道】", "【Nghệ thuật dùng người & lãnh đạo】"),
        ("【外出气场】", "【Khí trường khi ra ngoài phát triển】"),
        ("【异地机遇】", "【Cơ hội phương xa】"),
        ("【出行平安】", "【An toàn di chuyển】"),
        ("【子女缘分】", "【Duyên phận đường con cái】"),
        ("【育儿方针】", "【Định hướng giáo dục con cái】"),
        ("【原生家庭】", "【Nền tảng gia đình & cha mẹ】"),
        ("【长辈贵人】", "【Quý nhân trưởng bối / Thượng cấp】"),
        ("【孝道提醒】", "【Lưu ý chăm sóc sức khỏe cha mẹ】"),
        ("【核心定位】", "【Định vị sự nghiệp cốt lõi】"),
        ("【黄金组合】", "【Tổ hợp sao vàng】"),
        ("【避坑指南】", "【Cẩm nang phòng tránh rủi ro】"),
        ("【进财模式】", "【Mô thức tạo dựng tài lộc】"),
        ("【财富来源】", "【Nguồn gốc tài phú】"),
        ("【守财铁律】", "【Nguyên tắc giữ tiền & đầu tư】"),
        ("【精神底色】", "【Nền tảng tinh thần & nội tâm】"),
        ("【福报来源】", "【Nguồn phúc báo】"),
        ("【心力养护】", "【Nuôi dưỡng tâm thức】"),
        ("【深度优势】", "【Ưu thế chiều sâu】"),
        ("【特殊格局】", "【Cách cục đặc biệt】"),
        ("【能量转化】", "【Chuyển hóa năng lượng】"),
        ("《紫微斗数全书", "《Tử Vi Đẩu Số Toàn Thư"),
        ("命宫", "cung Mệnh"), ("身宫", "Thân cung"), ("兄弟宫", "cung Huynh Đệ"),
        ("夫妻宫", "cung Phu Thê"), ("子女宫", "cung Tử Tức"), ("财帛宫", "cung Tài Bạch"),
        ("疾厄宫", "cung Tật Ách"), ("迁移宫", "cung Thiên Di"), ("交友宫", "cung Giao Hữu (Nô Bộc)"),
        ("官禄宫", "cung Quan Lộc"), ("田宅宫", "cung Điền Trạch"), ("福德宫", "cung Phúc Đức"),
        ("父母宫", "cung Phụ Mẫu"), ("来因宫", "Lai Nhân Cung"), ("身居官禄", "Thân cư Quan Lộc"),
        ("身居财帛", "Thân cư Tài Bạch"), ("身居夫妻", "Thân cư Phu Thê"), ("身居迁移", "Thân cư Thiên Di"),
        ("身居福德", "Thân cư Phúc Đức"), ("身命同宫", "Thân Mệnh đồng cung"),
        ("紫微", "Tử Vi"), ("天机", "Thiên Cơ"), ("太阳", "Thái Dương"), ("武曲", "Vũ Khúc"),
        ("天同", "Thiên Đồng"), ("廉贞", "Liêm Trinh"), ("天府", "Thiên Phủ"), ("太阴", "Thái Âm"),
        ("贪狼", "Tham Lang"), ("巨门", "Cự Môn"), ("天相", "Thiên Tướng"), ("天梁", "Thiên Lương"),
        ("七杀", "Thất Sát"), ("破军", "Phá Quân"), ("禄存", "Lộc Tồn"), ("天马", "Thiên Mã"),
        ("左辅", "Tả Phù"), ("右弼", "Hữu Bật"), ("文昌", "Văn Xương"), ("文曲", "Văn Khúc"),
        ("天魁", "Thiên Khôi"), ("天钺", "Thiên Việt"), ("火星", "Hỏa Tinh"), ("铃星", "Linh Tinh"),
        ("擎羊", "Kình Dương"), ("陀罗", "Đà La"), ("地空", "Địa Không"), ("地劫", "Địa Kiếp"),
        ("化禄", "Hóa Lộc"), ("化权", "Hóa Quyền"), ("化科", "Hóa Khoa"), ("化忌", "Hóa Kỵ"),
        ("红鸾", "Hồng Loan"), ("天喜", "Thiên Hỷ"), ("天刑", "Thiên Hình"), ("天姚", "Thiên Diêu"),
        ("庙旺", "Miếu Vượng"), ("入庙", "Nhập Miếu"), ("得地", "Đắc Địa"), ("落陷", "Lạc Hãm"),
        ("倪师", "Đại sư Nghê Hải Hạ"), ("天纪", "Thiên Kỷ"),
    ]

    for line in lines:
        s = line.strip()
        if not s:
            out_lines.append("")
            continue
        if s in tm:
            out_lines.append(tm[s])
            continue
        t = s
        for cn, vi in replacements:
            t = t.replace(cn, vi)
        out_lines.append(t)

    return "\n".join(out_lines)


def main():
    parser = argparse.ArgumentParser(description="Tu Vi Thien Ky CLI — Trích xuất Kho 56.6 GB (100% Tiếng Việt)")
    parser.add_argument("--name", required=True, help="Họ và tên đương số")
    parser.add_argument("--gender", choices=["male", "female"], required=True, help="Giới tính: male (Nam) hoặc female (Nữ)")
    parser.add_argument("--day", type=int, required=True, help="Ngày sinh Dương lịch (1-31)")
    parser.add_argument("--month", type=int, required=True, help="Tháng sinh Dương lịch (1-12)")
    parser.add_argument("--year", type=int, required=True, help="Năm sinh Dương lịch (1920-2030)")
    parser.add_argument("--hour-idx", type=int, default=None, help="Chỉ số giờ Chi (0=Tý .. 11=Hợi)")
    parser.add_argument("--clock-time", type=str, default=None, help="Giờ sinh đồng hồ HH:MM để tính Chân Thái Dương Thời")
    parser.add_argument("--province", type=str, default="Hà Nội", help="Tỉnh/Thành phố sinh (để lấy kinh độ chính xác)")
    parser.add_argument("--custom-lon", type=float, default=None, help="Kinh độ tùy chỉnh (độ Đông)")
    parser.add_argument("--out-dir", type=str, default=DEFAULT_OUT_DIR, help="Thư mục xuất file")

    args = parser.parse_args()

    lon = args.custom_lon if args.custom_lon is not None else VN_PROVINCES_LON.get(args.province.strip().lower(), 105.834)

    if args.clock_time:
        parts = args.clock_time.split(":")
        hh = int(parts[0])
        mm = int(parts[1]) if len(parts) > 1 else 0
        tst_info = calc_true_solar_time(args.year, args.month, args.day, hh, mm, lon)
        hour_idx = tst_info["hour_idx"]
    elif args.hour_idx is not None:
        hour_idx = int(args.hour_idx) % 12
        hh = (hour_idx * 2) % 24
        tst_info = calc_true_solar_time(args.year, args.month, args.day, hh, 0, lon)
        tst_info["hour_idx"] = hour_idx
        tst_info["chi_name"] = CHI_NAMES[hour_idx]
        tst_info["chi_range"] = CHI_RANGES[hour_idx]
    else:
        raise ValueError("Cần cung cấp --hour-idx (0..11) hoặc --clock-time (HH:MM)")

    print(f"==================================================")
    print(f"  TỬ VI ĐẨU SỐ THIÊN KỶ — TRÍCH XUẤT 56.6 GB")
    print(f"==================================================")
    print(f"Đương số    : {args.name} ({'Nam' if args.gender == 'male' else 'Nữ'})")
    print(f"Ngày sinh DL: {args.day:02d}/{args.month:02d}/{args.year:04d}")
    print(f"Địa điểm    : {args.province} (Kinh độ {lon:.3f}°E)")
    print(f"Chân Thái Dương: Giờ {tst_info['chi_name']} ({tst_info['chi_range']}, hour_idx={hour_idx})")

    rec = extract_record_from_zst(args.year, args.month, args.day, hour_idx, args.gender)

    tm_path = os.path.join(ASSETS_DIR, "vi_translation_memory.json")
    tm = {}
    if os.path.exists(tm_path):
        with open(tm_path, encoding="utf-8") as f:
            tm = json.load(f)

    slug = slugify(args.name)
    folder_name = f"{slug}_{args.year}_{hour_idx}_{args.gender}"
    target_dir = os.path.join(args.out_dir, folder_name)
    os.makedirs(target_dir, exist_ok=True)

    raw_path = os.path.join(target_dir, f"raw_{rec['id']}.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)

    vi_13d = {}
    for k, val in rec.get("c", {}).items():
        if isinstance(val, str):
            vi_13d[k] = translate_cn_to_vi_fallback(val, tm)

    vi_path = os.path.join(target_dir, f"vi_13d_{rec['id']}.json")
    with open(vi_path, "w", encoding="utf-8") as f:
        json.dump({
            "id": rec["id"],
            "name": args.name,
            "gender": args.gender,
            "province": args.province,
            "tst_info": tst_info,
            "meta": rec.get("m", {}),
            "vi_13d": vi_13d,
        }, f, ensure_ascii=False, indent=2)

    print(f"[+] Dữ liệu gốc 56.6 GB : {raw_path}")
    print(f"[+] Bản dịch 13 chiều   : {vi_path}")
    print(f"[+] Hoàn tất thành công!")


if __name__ == "__main__":
    main()
