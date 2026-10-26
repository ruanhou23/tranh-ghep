#!/usr/bin/env python3
"""
Tải 100 ảnh Doraemon chất lượng cao từ Doraemon Wiki & Wikimedia Commons
làm kho ảnh mảnh ghép (tiles) cho dự án mosaic.
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from PIL import Image
import io
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiles_doraemon")
TARGET_COUNT = 100

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://doraemon.fandom.com/",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def download_image_bytes(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

def get_doraemon_fandom_urls(needed=200):
    urls = []
    api_url = f"https://doraemon.fandom.com/api.php?action=query&list=allimages&ailimit={min(needed, 250)}&aiprop=url|mime|dimensions&format=json"
    try:
        data = fetch_json(api_url)
        images = data.get("query", {}).get("allimages", [])
        for img in images:
            mime = img.get("mime", "")
            w = img.get("width", 0)
            h = img.get("height", 0)
            url = img.get("url", "")
            if mime in ["image/jpeg", "image/png", "image/webp"] and w >= 80 and h >= 80 and url:
                urls.append(url)
    except Exception as e:
        print(f"Lỗi khi gọi Doraemon Fandom API: {e}", file=sys.stderr)
    return urls

def get_wikimedia_urls(needed=100):
    urls = []
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=Doraemon&gsrlimit={needed}&prop=imageinfo&iiprop=url|mime|dimensions&format=json"
    try:
        data = fetch_json(api_url)
        pages = data.get("query", {}).get("pages", {})
        for page_id, page in pages.items():
            infos = page.get("imageinfo", [])
            if not infos:
                continue
            info = infos[0]
            mime = info.get("mime", "")
            w = info.get("width", 0)
            h = info.get("height", 0)
            url = info.get("url", "")
            if mime in ["image/jpeg", "image/png", "image/webp"] and w >= 80 and h >= 80 and url:
                urls.append(url)
    except Exception as e:
        print(f"Lỗi khi gọi Wikimedia API: {e}", file=sys.stderr)
    return urls

def process_and_save(url, target_path):
    try:
        raw_data = download_image_bytes(url)
        img = Image.open(io.BytesIO(raw_data))
        img = img.convert("RGB")
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        img = img.resize((150, 150), Image.LANCZOS)
        img.save(target_path, "JPEG", quality=90)
        return True, url, (img.width, img.height)
    except Exception as e:
        return False, url, str(e)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 60)
    print(" Bắt đầu tải kho ảnh Doraemon...")
    print(f"📁 Thư mục lưu: {OUTPUT_DIR}")
    print("=" * 60)

    urls = get_doraemon_fandom_urls(200)
    if len(urls) < 150:
        urls.extend(get_wikimedia_urls(60))

    urls = list(dict.fromkeys(urls))
    print(f" Tìm thấy {len(urls)} ảnh ứng viên. Đang tải {TARGET_COUNT} ảnh...")

    saved_count = 0
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_url = {}
        for idx, u in enumerate(urls):
            tmp_path = os.path.join(OUTPUT_DIR, f"temp_{idx:04d}.jpg")
            future_to_url[executor.submit(process_and_save, u, tmp_path)] = (idx, tmp_path)

        for future in as_completed(future_to_url):
            success, u, res = future.result()
            idx, tmp_path = future_to_url[future]
            if success:
                saved_count += 1
                final_path = os.path.join(OUTPUT_DIR, f"doraemon_{saved_count:03d}.jpg")
                if os.path.exists(tmp_path):
                    os.replace(tmp_path, final_path)
                print(f"[{saved_count:03d}/{TARGET_COUNT}] Đã lưu: doraemon_{saved_count:03d}.jpg", flush=True)
                if saved_count >= TARGET_COUNT:
                    break
            else:
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass

    # Dọn dẹp các file temp còn sót lại
    for f in os.listdir(OUTPUT_DIR):
        if f.startswith("temp_"):
            try:
                os.remove(os.path.join(OUTPUT_DIR, f))
            except Exception:
                pass

    final_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("doraemon_") and f.endswith(".jpg")]
    print("=" * 60)
    print(f"🎉 Hoàn tất! Đã tải thành công {len(final_files)} ảnh Doraemon vào thư mục:")
    print(f"   {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
