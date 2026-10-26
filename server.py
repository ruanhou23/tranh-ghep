#!/usr/bin/env python3
"""
Mosaic Web UI Server
Chạy server cục bộ để trải nghiệm ứng dụng web trực quan tạo ảnh Photo Mosaic.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Hiển thị log gọn gàng
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

def main():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print(f" Photo Mosaic Web Server đang chạy tại: {url}")
        print(" Nhấn Ctrl+C để dừng server.")
        print("=" * 60)
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã tắt server.")

if __name__ == "__main__":
    main()
