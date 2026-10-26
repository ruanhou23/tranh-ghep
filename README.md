# tranh-ghep (Photo Mosaic Studio)

Ứng dụng tạo ảnh ghép nghệ thuật (Photo Mosaic) trực quan và linh hoạt, hỗ trợ cả giao diện Web thời gian thực và dòng lệnh Python đa tiến trình.

## ✨ Tính năng chính

- **Giao diện Web trực quan (`index.html`)**:
  - Xem trực tiếp quá trình ghép ảnh từng dòng lên Canvas trong thời gian thực.
  - Tích hợp thanh trượt so sánh **Trước / Sau** (Split Comparison Slider).
  - Công cụ thu phóng $100\% - 400\%$ để soi chi tiết từng mảnh ghép (tile).
  - Tùy chỉnh kích thước mảnh ghép (Tile Size), độ chi tiết so khớp (Match Resolution), độ hòa trộn màu gốc (Color Overlay).
  - Nút xuất và tải ảnh chất lượng cao về máy.
  - Sẵn sàng với 1-click: Tạo ảnh mẫu hoặc nạp kho 100 ảnh Doraemon.

- **Kho 100 ảnh Doraemon chuẩn hóa (`tiles_doraemon/`)**:
  - Đã tích hợp sẵn 100 ảnh Doraemon độ phân giải chuẩn hóa $150 \times 150$ để chạy thử nghiệm ngay lập tức.
  - Kèm script tự động tải và cập nhật kho ảnh từ Wiki/Commons: `download_doraemon.py`.

- **Xử lý dòng lệnh đa luồng CPU (`mosaic.py`)**:
  - Tận dụng tối đa các nhân CPU của máy chủ/máy tính cá nhân để tạo các bức ảnh mosaic kích thước lớn nhanh chóng.

---

## 🚀 Hướng dẫn sử dụng

### Cách 1: Sử dụng giao diện Web (Khuyên dùng)

1. Khởi động server nội bộ:
```bash
python3 server.py
```
2. Trình duyệt sẽ tự động mở tại `http://localhost:8000`. Bạn cũng có thể mở trực tiếp file `index.html` trên bất kỳ trình duyệt nào mà không cần cài đặt thêm phần mềm.

### Cách 2: Chạy qua dòng lệnh (CLI)

```bash
python3 mosaic.py <ảnh_gốc> <thư_mục_tiles>
```

**Ví dụ:**
```bash
python3 mosaic.py tiles_doraemon/doraemon_001.jpg tiles_doraemon
```
Kết quả mosaic sẽ được lưu vào file `mosaic.jpeg`.

### Tải lại hoặc bổ sung thêm ảnh Doraemon
```bash
python3 download_doraemon.py
```

---

## 🛠️ Yêu cầu môi trường
- Python 3.8+
- Thư viện: `Pillow` (`pip install Pillow`)

---

## 📄 Bản quyền & Tham khảo
Phát triển và mở rộng từ [codebox/mosaic](https://github.com/codebox/mosaic).
