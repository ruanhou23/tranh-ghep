#!/usr/bin/env python3
"""
Đăng nhập GitHub qua trình duyệt Chrome bằng GitHub Device Authorization Flow
và tự động push dự án lên GitHub.
"""
import sys
import os
import json
import time
import urllib.request
import urllib.parse
import webbrowser
import subprocess

CLIENT_ID = "178c6fc778ccc68e1d6a" # GitHub CLI client_id
REPO_URL = "https://github.com/ruanhou23/tranh-ghep.git"
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def get_device_code():
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "scope": "repo,workflow"
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://github.com/login/device/code",
        data=data,
        headers={"Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def poll_for_token(device_code, interval=5, expires_in=900):
    start_time = time.time()
    poll_interval = max(interval, 5)

    while time.time() - start_time < expires_in:
        time.sleep(poll_interval)
        data = urllib.parse.urlencode({
            "client_id": CLIENT_ID,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://github.com/login/oauth/access_token",
            data=data,
            headers={"Accept": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                if "access_token" in res:
                    return res["access_token"]
                err = res.get("error")
                if err == "authorization_pending":
                    print(".", end="", flush=True)
                    continue
                elif err == "slow_down":
                    poll_interval += 5
                    continue
                elif err in ["expired_token", "access_denied"]:
                    print(f"\n❌ Lỗi: {err}")
                    return None
        except Exception as e:
            time.sleep(2)
            continue
    return None

def main():
    print("=" * 65)
    print("🚀 ĐĂNG NHẬP GITHUB QUA CHROME & TỰ ĐỘNG PUSH CODE")
    print("=" * 65)
    print("Đang khởi tạo phiên xác thực với GitHub...")

    info = get_device_code()
    user_code = info["user_code"]
    device_code = info["device_code"]
    verification_uri = info.get("verification_uri", "https://github.com/login/device")
    interval = info.get("interval", 5)

    print("\n" + "#" * 65)
    print(f"👉 1. Mở Chrome và vào liên kết: {verification_uri}")
    print(f"👉 2. Nhập mã kích hoạt sau:   {user_code}")
    print(f"👉 3. Bấm 'Authorize github' để hoàn tất đăng nhập.")
    print("#" * 65 + "\n")

    try:
        webbrowser.open(verification_uri)
    except Exception:
        pass

    print("⏳ Đang đợi bạn xác nhận trên Chrome", end="", flush=True)
    token = poll_for_token(device_code, interval=interval)

    if not token:
        print("\n❌ Không nhận được xác thực từ trình duyệt hoặc phiên đã hết hạn.")
        sys.exit(1)

    print(f"\n✅ Đã xác thực thành công tài khoản GitHub!")
    print("🚀 Đang tự động đẩy mã nguồn lên GitHub...")

    # Configure authenticated remote
    auth_remote = f"https://{token}@github.com/ruanhou23/tranh-ghep.git"
    os.chdir(REPO_DIR)

    res = subprocess.run(["git", "remote", "set-url", "origin", auth_remote], capture_output=True, text=True)
    push_res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)

    # Clean token from git config origin URL for security
    subprocess.run(["git", "remote", "set-url", "origin", REPO_URL], capture_output=True, text=True)

    if push_res.returncode == 0:
        print("\n" + "=" * 65)
        print("🎉 THÀNH CÔNG RỰC RỠ!")
        print(f"Toàn bộ mã nguồn đã được tải lên kho GitHub:")
        print(f"🔗 {REPO_URL}")
        print("=" * 65)
    else:
        print("\n❌ Lỗi khi push code:")
        print(push_res.stderr or push_res.stdout)

if __name__ == "__main__":
    main()
