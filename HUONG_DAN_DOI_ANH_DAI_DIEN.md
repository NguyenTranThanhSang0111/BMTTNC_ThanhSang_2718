# Hướng dẫn thay đổi ảnh đại diện

## Cách 1: Thay đổi ảnh đại diện (Khuyến nghị)

### Bước 1: Chuẩn bị ảnh
- Kích thước: 200x200px hoặc 400x400px (hình vuông)
- Format: PNG hoặc JPG
- Nên sử dụng ảnh có nền trong suốt (PNG) hoặc nền đơn giản

### Bước 2: Đặt ảnh vào thư mục
1. Copy file ảnh của bạn
2. Đặt vào thư mục: `static/images/`
3. Đổi tên file thành: `avatar.png` (hoặc `avatar.jpg`)

**Ví dụ:**
```
static/images/avatar.png
```

### Bước 3: Kiểm tra cấu hình
Mở file `hugo.toml` và kiểm tra dòng 178:
```toml
avatarURL = "/images/avatar.png"
```

Nếu bạn dùng file `.jpg`, sửa thành:
```toml
avatarURL = "/images/avatar.jpg"
```

### Bước 4: Xem kết quả
- Nếu đang chạy `hugo server`, refresh trình duyệt (Ctrl + F5)
- Nếu đã deploy lên GitHub Pages, push code lên GitHub để tự động cập nhật

---

## Cách 2: Sử dụng ảnh từ URL bên ngoài

### Bước 1: Upload ảnh lên dịch vụ lưu trữ
- GitHub: Upload vào repository và lấy link
- Imgur: Upload và lấy direct link
- Cloudinary: Upload và lấy URL

### Bước 2: Cập nhật trong hugo.toml
Mở file `hugo.toml` và sửa dòng 178:
```toml
avatarURL = "https://example.com/path/to/your/avatar.png"
```

**Ví dụ:**
```toml
avatarURL = "https://i.imgur.com/your-image.png"
```

---

## Cách 3: Sử dụng Gravatar

### Bước 1: Đăng ký Gravatar
1. Truy cập: https://gravatar.com
2. Đăng ký tài khoản với email của bạn
3. Upload ảnh đại diện

### Bước 2: Cấu hình trong hugo.toml
Mở file `hugo.toml` và điền email vào dòng 176:
```toml
gravatarEmail = "your-email@example.com"
```

**Lưu ý:** Nếu đã điền `gravatarEmail`, hệ thống sẽ ưu tiên sử dụng Gravatar thay vì `avatarURL`.

---

## Lưu ý quan trọng

1. **Đường dẫn ảnh:**
   - Đường dẫn tương đối: `/images/avatar.png` (cho local và GitHub Pages)
   - Đường dẫn tuyệt đối: `https://example.com/images/avatar.png` (cho production)

2. **Kích thước file:**
   - Nên giữ file ảnh dưới 500KB để tải nhanh
   - Sử dụng công cụ nén ảnh: TinyPNG, Squoosh

3. **Sau khi thay đổi:**
   - Nếu chạy local: Refresh trình duyệt (Ctrl + F5 để xóa cache)
   - Nếu deploy GitHub Pages: Push code lên GitHub, đợi 2-5 phút để deploy

4. **Kiểm tra:**
   - Ảnh đại diện hiển thị trên trang chủ
   - Ảnh hiển thị đúng, không bị vỡ
   - Ảnh tải nhanh

---

## Công cụ hỗ trợ

### Resize ảnh online:
- **Photopea**: https://www.photopea.com (miễn phí, giống Photoshop)
- **Canva**: https://www.canva.com (dễ sử dụng)
- **Squoosh**: https://squoosh.app (Google, nén và resize ảnh)

### Nén ảnh:
- **TinyPNG**: https://tinypng.com
- **Squoosh**: https://squoosh.app

---

## Ví dụ thực tế

### Thay đổi từ ảnh cũ sang ảnh mới:

1. **Copy ảnh mới:**
   ```powershell
   Copy-Item "C:\Users\YourName\Pictures\new-avatar.jpg" -Destination "static\images\avatar.png"
   ```

2. **Kiểm tra file:**
   ```powershell
   Get-ChildItem "static\images\avatar.*"
   ```

3. **Commit và push:**
   ```bash
   git add static/images/avatar.png
   git commit -m "Update avatar image"
   git push
   ```

---

## Troubleshooting

### Vấn đề: Ảnh không hiển thị
- ✅ Kiểm tra đường dẫn trong `hugo.toml` có đúng không
- ✅ Kiểm tra file ảnh có tồn tại trong `static/images/` không
- ✅ Xóa cache trình duyệt (Ctrl + F5)
- ✅ Kiểm tra tên file có đúng không (phân biệt hoa thường)

### Vấn đề: Ảnh hiển thị nhưng bị mờ
- ✅ Sử dụng ảnh có độ phân giải cao hơn (400x400px thay vì 200x200px)
- ✅ Kiểm tra ảnh không bị nén quá mức

### Vấn đề: Ảnh quá lớn, tải chậm
- ✅ Nén ảnh bằng TinyPNG hoặc Squoosh
- ✅ Chuyển sang format JPG thay vì PNG (nếu không cần nền trong suốt)

---

## Tóm tắt nhanh

1. **Copy ảnh** → `static/images/avatar.png`
2. **Kiểm tra** `hugo.toml` dòng 178: `avatarURL = "/images/avatar.png"`
3. **Refresh** trình duyệt hoặc **push** lên GitHub

Xong! 🎉

