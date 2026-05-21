# Multi-Token Voice 24/7

Tài liệu này hướng dẫn cài đặt và chạy tool trên cả Windows, macOS, Linux và VPS.

> Hướng dẫn treo VPS 24/7: [GUIDE_VN.md](GUIDE_VN.md)

## Lưu Ý Quan Trọng

Tool này dùng token tài khoản Discord và hoạt động theo kiểu self-bot. Việc tự động hóa tài khoản người dùng có thể vi phạm Điều khoản Dịch vụ của Discord và có thể làm tài khoản bị hạn chế. Hãy tự chịu trách nhiệm khi sử dụng.

Không chia sẻ các file có token như `tokens.txt`, `dead_tokens.txt`, `token_details.csv`, `evs.txt`, `user_info.txt`.

## Tool Này Dùng Để Làm Gì?

- Đăng nhập nhiều token Discord từ file `tokens.txt`.
- Cho nhiều tài khoản vào một hoặc nhiều voice channel.
- Tự chia đều token vào nhiều channel ở Normal Mode.
- Hỗ trợ Auto-Room: cho token leader vào lobby, sau đó phân phối token còn lại vào room mới.
- Có menu điều khiển trong terminal: bật/tắt mic, camera, deaf, reaction, đổi nickname, thoát.
- Có cơ chế duy trì kết nối voice và tự kết nối lại khi có lỗi mạng/socket.

## Cấu Trúc File

```text
.
├── self-bot.py                  # File chạy chính
├── run.bat                      # Chạy nhanh trên Windows
├── run.sh                       # Chạy nhanh trên macOS/Linux/VPS
├── requirements.txt             # Danh sách thư viện Python
├── tokens.txt                   # Danh sách token, mỗi dòng một token
├── docs/
│   ├── README_VN.md             # Tài liệu tiếng Việt
│   └── GUIDE_VN.md              # Hướng dẫn treo VPS 24/7
└── Token Tools/
    ├── get_token.py             # Đăng nhập browser để lấy token và user info
    ├── check_info_token.py      # Check token sống/chết và xuất thông tin
    └── browser_login.py         # Test đăng nhập Discord bằng token trên Chrome
```

## Yêu Cầu

- Python 3.8 trở lên.
- Git nếu tải source bằng lệnh `git clone`.
- Chrome/Chromium nếu dùng các script trong thư mục `Token Tools/`.

Kiểm tra Python:

```bash
python --version
python3 --version
```

Windows thường dùng `python`. macOS/Linux thường dùng `python3`.

## Bước 1: Tạo File Token

Tạo file `tokens.txt` ở thư mục gốc, cùng cấp với `self-bot.py`.

Ví dụ:

```text
TOKEN_1
TOKEN_2
TOKEN_3
```

Quy tắc:

- Mỗi dòng là một token.
- Không thêm dấu ngoặc kép.
- Không gửi file này cho người khác.
- Không đẩy file này lên GitHub.

## Bước 2: Gán OWNER_ID

Một số lệnh nhạy cảm chỉ cho phép chủ tool sử dụng.

1. Mở Discord.
2. Vào `User Settings` -> `Advanced`.
3. Bật `Developer Mode`.
4. Nhấn chuột phải vào tài khoản của bạn, chọn `Copy ID`.
5. Mở `self-bot.py`.
6. Tìm dòng này trong class `VoiceClone`:

```py
OWNER_ID: int = 1119601947683590145
```

Thay số đó bằng Discord User ID của bạn, lưu file rồi chạy lại bot.

## Cách Chạy Nhanh

### Windows

Nhấn đúp vào `run.bat`, hoặc mở CMD/PowerShell tại thư mục tool và chạy:

```cmd
run.bat
```

File này sẽ tự tạo `venv`, cài thư viện và chạy `self-bot.py`.

### macOS / Linux / VPS

Chạy:

```bash
chmod +x run.sh
./run.sh
```

File này sẽ tự tạo `venv`, cài thư viện và chạy `self-bot.py`.

## Cài Đặt Thủ Công

Dùng phần này nếu file chạy nhanh bị lỗi hoặc bạn muốn tự cài.

### Windows CMD

```cmd
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python self-bot.py
```

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python self-bot.py
```

Nếu PowerShell báo không cho chạy script, chạy lệnh này:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Sau đó tắt PowerShell, mở lại và kích hoạt venv lần nữa.

### macOS

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 self-bot.py
```

Nếu máy chưa có Python, cài từ https://www.python.org/ hoặc Homebrew.

### Linux / VPS Ubuntu, Debian

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 self-bot.py
```

### Linux Fedora, CentOS, RHEL

```bash
sudo dnf install -y python3 python3-pip python3-devel
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 self-bot.py
```

## Cách Sử Dụng Khi Bot Chạy

Sau khi chạy `self-bot.py`, tool sẽ hỏi theo thứ tự:

1. Chọn chế độ:
   - `1` Normal Mode: nhập voice channel ID, tool chia đều token vào các channel.
   - `2` Auto-Room: token leader vào lobby trước, sau đó tool phân phối token còn lại vào room mới.
2. Chọn tốc độ login:
   - Nhấn Enter hoặc nhập `N`: Safe Mode, delay 8 giây.
   - Nhập `y`: Turbo Mode, delay 3 giây.
3. Nhập voice channel ID:
   - Một channel: `123456789012345678`
   - Nhiều channel: `123456789012345678 987654321098765432`
4. Dùng menu điều khiển:
   - `1` Toggle Mic cho tất cả tài khoản.
   - `2` Toggle Camera cho tất cả tài khoản.
   - `3` Toggle Deaf cho tất cả tài khoản.
   - `4` Spam Reaction vào một message.
   - `5` Đổi nickname toàn bộ tài khoản trong server.
   - `6` Thoát.

## Treo 24/7 Trên VPS

Nếu chạy trên VPS, nên dùng `screen` để bot vẫn chạy sau khi bạn tắt SSH:

```bash
screen -S discord_voice
source venv/bin/activate
python3 self-bot.py
```

Để thoát khỏi màn hình `screen` mà không tắt bot:

```text
Ctrl + A, sau đó nhấn D
```

Vào lại bot:

```bash
screen -r discord_voice
```

Xem hướng dẫn đầy đủ tại [GUIDE_VN.md](GUIDE_VN.md).

## Token Tools

Cài thư viện trước:

```bash
pip install -r requirements.txt
```

Check token sống/chết và xuất thông tin:

```bash
python "Token Tools/check_info_token.py"
```

Test đăng nhập Discord bằng token trên Chrome:

```bash
python "Token Tools/browser_login.py"
python "Token Tools/browser_login.py" "YOUR_TOKEN_HERE"
```

Mở Chrome, đăng nhập thủ công rồi lưu token/user info:

```bash
python "Token Tools/get_token.py"
```

Ghi chú:

- `get_token.py` hiện đang cấu hình Chrome Linux ở đường dẫn `/usr/bin/google-chrome`.
- Các tool browser cần Chrome/Chromium.
- File kết quả có thể chứa token hoặc thông tin tài khoản, cần giữ riêng tư.

## Lỗi Thường Gặp

### `File tokens.txt not found`

Tạo file `tokens.txt` cùng thư mục với `self-bot.py`.

### `No tokens found`

Kiểm tra `tokens.txt` có token chưa, mỗi token phải nằm trên một dòng riêng.

### Windows báo không nhận lệnh `python`

Cài lại Python từ https://www.python.org/ và nhớ tick `Add Python to PATH`, sau đó mở lại CMD/PowerShell.

### Ubuntu/Debian lỗi khi tạo venv

Cài thêm gói venv:

```bash
sudo apt install -y python3-venv python3-pip
```

### PowerShell không kích hoạt được venv

Chạy:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Lỗi Chrome driver khi dùng Token Tools

Cài Chrome/Chromium và driver. Trên Ubuntu/Debian có thể dùng:

```bash
sudo apt install -y chromium chromium-driver
```

## Ủng Hộ

- Star repo nếu tool hữu ích.
- Discord support: https://discord.gg/mgl

Phát triển bởi `kwishtt`.
