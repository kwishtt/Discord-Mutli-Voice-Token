# HƯỚNG DẪN TREO BOT 24/24 (AN TOÀN TUYỆT ĐỐI)

Hướng dẫn này giúp anh chạy bot độc lập, không cài rác vào máy tính/VPS gốc (bảo vệ hệ điều hành) và giữ bot chạy ngay cả khi anh tắt máy tính hoặc mất mạng.

## PHẦN 1: Cài đặt Môi trường (Chỉ làm 1 lần)

Đây là bước tạo "ngôi nhà riêng" (venv) cho bot. Nếu bot lỗi, chỉ cần xóa thư mục `venv` là xong, máy tính vẫn sạch sẽ.

**Bước 1: Dọn dẹp cũ (cho chắc ăn)**
```bash
rm -rf venv
```

**Bước 2: Tạo môi trường ảo (Virtual Environment)**
```bash
python3 -m venv venv
```

**Bước 3: Kích hoạt môi trường**
*Khi kích hoạt, dòng lệnh sẽ hiện chữ `(venv)` ở đầu.*
```bash
source venv/bin/activate
```

**Bước 4: Cài đặt thư viện**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
*(Chờ nó chạy xong, nếu thấy báo "Successfully installed..." là ngon)*

---

## PHẦN 2: Treo Bot 24/24 với `screen`

Do bot của anh cần nhập ID kênh và chọn chế độ khi khởi động, nên dùng `screen` là tốt nhất. Nó giống như anh mở một cửa sổ ảo, chạy bot đó, rồi "thu nhỏ" nó lại để nó chạy ngầm.

**Bước 1: Tạo cửa sổ ảo mới**
```bash
screen -S discord_bot
```
*(Lúc này màn hình sẽ xóa trắng, anh đang ở trong cửa sổ ảo)*

**Bước 2: Chạy bot**
Nếu chưa kích hoạt venv thì kích hoạt lại:
```bash
source venv/bin/activate
python3 self-bot.py
```

**Bước 3: Nhập thông tin**
- Nhập list ID kênh.
- Chọn chế độ (Safe/Turbo).
- Đợi bot báo "Started" và hiện Menu điều khiển.

**Bước 4: "Thoát ly" (Detach)**
Để giữ bot chạy ngầm và quay lại màn hình chính của anh:
- Nhấn giữ **Ctrl**, ấn **A**, rồi thả cả hai ra.
- Ấn phím **D**.
*(Màn hình sẽ báo `[detached]`, bot vẫn đang chạy ngầm)*

---

## PHẦN 3: Quản lý Bot đang treo

**1. Kiểm tra xem bot còn sống không**
```bash
screen -ls
```
Anh sẽ thấy dòng kiểu `12345.discord_bot (Detached)`.

**2. Quay lại màn hình bot (để chỉnh hoặc tắt)**
```bash
screen -r discord_bot
```

**3. Tắt hẳn bot**
- Vào lại màn hình bot (`screen -r discord_bot`).
- Trong menu bot chọn Exit, hoặc ấn **Ctrl + C**.
- Gõ `exit` để đóng luôn cửa sổ `screen`.

### 🚑 CỨU HỘ: KHI KHÔNG VÀO ĐƯỢC SCREEN
Nếu anh thấy báo `Attached` mà không vào được, hoặc quá nhiều screen trùng tên:

**Cách 1: Ép vào (Force Detach)**
Dùng lệnh này để "đá" phiên đăng nhập cũ ra và nhảy vào lại:
```bash
screen -d -r discord_bot
# Hoặc dùng ID cụ thể (xem ID bằng screen -ls)
screen -d -r 12345
```

**Cách 2: Diệt sạch (Làm lại cuộc đời)**
Nếu loạn quá, dùng lệnh này xóa sạch toàn bộ screen cũ đi để chạy lại từ đầu:

```bash
pkill screen
# Hoặc xóa cụ thể các screen đã chết
screen -wipe
```

---

## TÓM TẮT LỆNH NHANH
Mỗi lần khởi động lại VPS chỉ cần:
1. `screen -S discord_bot`
2. `source venv/bin/activate`
3. `python3 self-bot.py`
4. **Ctrl+A**, **D**
