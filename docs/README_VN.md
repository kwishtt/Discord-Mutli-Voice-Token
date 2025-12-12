# Multi-Token-Voice-24/24

Hệ thống quản lý và treo Voice Discord 24/7 cho nhiều tài khoản cùng lúc. Được tối ưu hóa cho hiệu suất cao và độ ổn định lâu dài trên Linux/VPS.

## Tài liệu chi tiết
*   [HƯỚNG DẪN TREO BOT 24/24 TRÊN VPS (GUIDE_VN.md)](GUIDE_VN.md) - Hướng dẫn chi tiết cách dùng `screen` để treo máy không cần bật PC.

## Tính năng chính

*   **Đa luồng (Multi-Token)**: Hỗ trợ đăng nhập và quản lý hàng loạt tài khoản (token) cùng một lúc.
*   **Kết nối bền vững (24/7)**: Tự động tham gia và duy trì kết nối voice channel không ngắt quãng. Tự động kết nối lại khi mạng lag hoặc lỗi socket.
*   **Chế độ thông minh (Safe/Turbo)**: 
    *   **Safe Mode**: Login chậm rãi, an toàn, tránh bị Discord quét checkpoint.
    *   **Turbo Mode**: Login tốc độ cao cho dàn bot số lượng lớn.
*   **Điều khiển tập trung**: Menu điều khiển trực tiếp (Mute, Deafen, Camera Toggle) cho toàn bộ dàn bot chỉ với một phím bấm.
*   **Tiết kiệm tài nguyên**: Tối ưu hóa để chạy mượt mà trên các VPS cấu hình thấp (1GB RAM).

## Cấu trúc thư mục

```text
.
├── docs/                # Tài liệu hướng dẫn
│   ├── GUIDE_VN.md      # Hướng dẫn treo máy chi tiết
│   └── README_VN.md     # File đọc này
├── Token Check/         # Công cụ kiểm tra và lọc token
├── self-bot.py          # Code chính chạy bot
├── run.sh               # Script tự động cài đặt và chạy
├── tokens.txt           # Danh sách token (Không được share file này)
└── requirements.txt     # Các thư viện Python cần thiết
```

## Hướng dẫn cài đặt

### Yêu cầu
*   **OS**: Linux (Ubuntu, Debian, CentOS...)
*   **Python**: 3.8 trở lên

### Các bước thực hiện

1.  **Cấu hình Token:**
    Tạo một file tên là `tokens.txt` ở thư mục gốc (cùng chỗ với `run.sh`), dán danh sách token vào, mỗi token một dòng.

2.  **Chạy lệnh cài đặt:**
    Cấp quyền và chạy script tự động:
    ```bash
    chmod +x run.sh
    ./run.sh
    ```

3.  **Vận hành:**
    
    *   **Với Linux / VPS:**
        ```bash
        chmod +x run.sh
        ./run.sh
        ```
    
    *   **Với Windows:**
        Chỉ cần click đúp vào file `run.bat` là xong. Nó sẽ tự cài môi trường và chạy bot.

### Cài đặt thủ công (Nếu script lỗi)

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

## Lưu ý quan trọng
Project này là **Self-bot**. Việc sử dụng self-bot có thể vi phạm Điều khoản Dịch vụ của Discord. Hãy sử dụng có trách nhiệm và không lạm dụng để spam.

---
*Phát triển bởi KTMJN Team*
*Tham gia Discord: discord.gg/mgl*