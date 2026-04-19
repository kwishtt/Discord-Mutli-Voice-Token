# Multi-Token-Voice-24/24

## 🆔 Cách gán `OWNER_ID` (Ghi chú quan trọng)

Một số lệnh nhạy cảm (spam chat) chỉ có thể dùng bởi `OWNER_ID` (ID người dùng của bạn). Hướng dẫn lấy và gán:

1. Trong Discord: `User Settings` → `Advanced` → bật **Developer Mode**.
2. Nhấn phải vào avatar của bạn (hoặc tên trong member list) → **Copy ID**.
3. Mở file `self-bot.py`, tìm hằng `OWNER_ID` trong lớp `VoiceClone` và thay giá trị bằng ID của bạn. Ví dụ:

```py
# inside self-bot.py
OWNER_ID: int = 1119601947683590145  # Thay bằng ID của bạn
```
Lưu file và khởi động lại bot.

## 📚 Tài liệu chi tiết
*   [HƯỚNG DẪN TREO BOT 24/24 TRÊN VPS (GUIDE_VN.md)](GUIDE_VN.md) - Hướng dẫn chi tiết cách dùng `screen` để treo máy không chạy ngầm khi tắt máy tính.

## 🌟 Tính năng chính

*   **🚀 Đa luồng (Multi-Token)**: Hỗ trợ đăng nhập và quản lý hàng loạt tài khoản (token) cùng một lúc.
*   **🔊 Kết nối bền vững (24/7)**: Tự động tham gia và duy trì kết nối voice channel không ngắt quãng. Tự động kết nối lại khi mạng lag hoặc lỗi socket.
*   **🧠 Chế độ thông minh (Safe/Turbo)**: 
    *   **Safe Mode**: Login chậm rãi, an toàn, tránh bị Discord quét checkpoint.
    *   **Turbo Mode**: Login tốc độ cao cho dàn bot số lượng lớn.
*   **🎮 Điều khiển tập trung**: Menu điều khiển trực tiếp (Mute, Deafen, Camera Toggle) cho toàn bộ dàn bot chỉ với một phím bấm.
*   **💾 Tiết kiệm tài nguyên**: Tối ưu hóa để chạy mượt mà trên các VPS cấu hình thấp (1GB RAM).

## Windows — Hướng dẫn cài đặt chi tiết

Nếu bạn chạy dự án trên Windows, làm theo các bước sau để cấu hình môi trường ổn định:

1. Tải và cài đặt Python 3.8+ từ https://www.python.org/ — trong quá trình cài đặt chọn "Add Python to PATH".

2. Mở Command Prompt hoặc PowerShell trong thư mục dự án (chạy dưới quyền Administrator nếu cần).

3. Tạo và kích hoạt virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

4. Cài thư viện cần thiết.

```powershell

pip install -r requirements.txt
```

5. Setup file token:
- Tạo 1 file `tokens.txt` tại cùng với thư mục hiện tại mà `self-bot.py` đang tồn tại. Dán token tài khoản thực thế của bạn vào, mỗi token đặt 1 dòng.

6. Chạy bot (hoặc dùng `run.bat`):

```powershell
python self-bot.py
# hoặc
.\\run.bat
```

7. Chạy tự động khi khởi động (tuỳ chọn): dùng Task Scheduler để tạo task chạy `python <đường_dẫn_đầy_đủ>\self-bot.py` khi đăng nhập, đặt working directory là thư mục dự án.

Ghi chú:
- Muốn chạy như service, cân nhắc `nssm` (Non-Sucking Service Manager) để đăng ký script như Windows service.
- Luôn giữ `tokens.txt` ở máy local và tuyệt đối không chia sẻ!!

## Linux Os - Hướng dẫn cài đặt

### Yêu cầu
*   **Python**: 3.8 trở lên

### Các bước thực hiện

1.  **Cấu hình Token:**
    Tạo một file tên là `tokens.txt` ở thư mục gốc (cùng chỗ với `run.sh`), dán danh sách token vào, mỗi token một dòng.

2.  **Vận hành:**
    
    *   **🐧 Với Linux / VPS:**
        ```bash
        chmod +x run.sh
        ./run.sh
        ```
    
    *   **🪟 Với Windows:**
        Chỉ cần click đúp vào file `run.bat` là xong. Nó sẽ tự cài môi trường và chạy bot.

### ⚙️ Cài đặt thủ công (Nếu script lỗi)

Nếu anh muốn tự tay cài đặt hoặc tool tự động bị lỗi, hãy làm theo các bước sau:

**Linux / MacOs:**
```bash
# 1. Tạo môi trường ảo
python3 -m venv venv

# 2. Kích hoạt môi trường
source venv/bin/activate

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Chạy bot
python3 self-bot.py
```

**Windows:**
```cmd
:: 1. Mở CMD tại thư mục, tạo venv
python -m venv venv

:: 2. Kích hoạt venv
venv\Scripts\activate

:: 3. Cài thư viện
pip install -r requirements.txt

:: 4. Chạy bot
python self-bot.py
```

    Làm theo hướng dẫn trên màn hình:
    *   Nhập ID phòng Voice.
    *   Chọn chế độ chạy (Safe/Turbo).
    
    > **Lưu ý:** Để treo máy 24/24 sau khi tắt máy tính (VPS), xem hướng dẫn tại [GUIDE_VN.md](GUIDE_VN.md).

## ⚠️ Lưu ý quan trọng

Project này là **Self-bot**. Việc sử dụng self-bot có thể vi phạm Điều khoản Dịch vụ của Discord. Hãy sử dụng có trách nhiệm và không lạm dụng để spam.

---
## ❤️ Ủng hộ / Donate
Nếu thấy tool này hữu ích, hãy ủng hộ chúng mình để có động lực phát triển thêm nhé!

*   **⭐ Star Project**: Tặng 1 sao cho repo này trên GitHub nhé!
*   **Discord**: Tham gia server giao lưu [discord.gg/mgl](https://discord.gg/mgl)

*Phát triển bởi kwishtt*


## 🧰 CÁC SCRIPT HỖ TRỢ

- `Token Check/browser_login.py`
    - Mục đích: Dùng `selenium` + `chromedriver` để inject token vào session trình duyệt và thử đăng nhập Discord. Tiện để kiểm tra token trong môi trường trình duyệt.
    - Chạy:
        ```bash
        python "Token Check/browser_login.py"
        # hoặc truyền token trực tiếp
        python "Token Check/browser_login.py" "YOUR_TOKEN_HERE"
        ```
    - Yêu cầu: `selenium`, Chrome/Chromium, `chromedriver`.

- `Token Check/cleaner.py`
    - Mục đích: Đọc `tokens.txt`, loại trùng, kiểm tra token hợp lệ bằng API Discord, lưu danh sách token hợp lệ vào `tokens.txt` (ghi đè), và xuất `dead_tokens.txt`, `tokens.bak`, `token_details.csv`.
    - Chạy:
        ```bash
        pip install -r requirements.txt
        python "Token Check/cleaner.py"
        ```

**Lưu ý bảo mật:** TUYỆT ĐỐI KHÔNG chia sẻ những file có chứa từ token đi bất cứ đâu, hãy lưu giữ nó ở máy của bạn. 
