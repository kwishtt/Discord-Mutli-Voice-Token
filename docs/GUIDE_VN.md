# Hướng Dẫn Treo Bot 24/7 Trên VPS

Tài liệu này dành cho Linux/VPS. Mục tiêu là chạy bot ổn định, tắt SSH vẫn không làm bot dừng, và có thể quay lại màn hình bot bất cứ lúc nào.

Nếu bạn chạy trên Windows hoặc macOS cá nhân thì đọc [README_VN.md](README_VN.md) trước.

## Cách Hoạt Động

Khi bạn SSH vào VPS và chạy bot trực tiếp, bot sẽ dừng nếu cửa sổ SSH bị đóng. `screen` tạo một terminal ảo trên VPS. Bot chạy trong terminal đó, còn bạn có thể thoát SSH mà bot vẫn tiếp tục chạy.

## Chuẩn Bị Lần Đầu

### 1. Cài Python và screen

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip screen
```

Fedora/CentOS/RHEL:

```bash
sudo dnf install -y python3 python3-pip python3-devel screen
```

### 2. Vào thư mục tool

Ví dụ:

```bash
cd ~/Discord_Voice
```

Nếu thư mục của bạn nằm chỗ khác, thay `~/Discord_Voice` bằng đường dẫn thật.

### 3. Tạo môi trường ảo

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Sau khi kích hoạt thành công, đầu dòng terminal thường có chữ `(venv)`.

### 4. Kiểm tra file token

File `tokens.txt` phải nằm cùng thư mục với `self-bot.py`.

```bash
ls -l tokens.txt self-bot.py
```

Nếu chưa có, tạo file:

```bash
nano tokens.txt
```

Dán token vào, mỗi dòng một token. Lưu trong nano bằng `Ctrl + O`, Enter, rồi thoát bằng `Ctrl + X`.

## Chạy Bot Bằng screen

### 1. Tạo phiên screen

```bash
screen -S discord_voice
```

Sau lệnh này, bạn đang ở trong một terminal ảo.

### 2. Chạy bot

Nếu chưa kích hoạt venv:

```bash
source venv/bin/activate
```

Chạy bot:

```bash
python3 self-bot.py
```

### 3. Nhập thông tin trong bot

Bot sẽ hỏi:

- Chế độ chạy:
  - `1` Normal Mode.
  - `2` Auto-Room.
- Tốc độ login:
  - Enter hoặc `N`: Safe Mode, delay 8 giây.
  - `y`: Turbo Mode, delay 3 giây.
- Voice channel ID:
  - Một channel: `123456789012345678`
  - Nhiều channel: `123456789012345678 987654321098765432`

Sau khi bot chạy xong phần login, bạn sẽ thấy menu điều khiển.

### 4. Thoát SSH mà vẫn giữ bot chạy

Nhấn:

```text
Ctrl + A
```

Thả tay ra, rồi nhấn:

```text
D
```

Nếu thấy `[detached]` nghĩa là bạn đã thoát khỏi screen, bot vẫn chạy trên VPS.

## Quản Lý Bot Đang Chạy

### Xem các phiên screen

```bash
screen -ls
```

Ví dụ kết quả:

```text
12345.discord_voice    (Detached)
```

`Detached` nghĩa là bot đang chạy nền.

### Vào lại màn hình bot

```bash
screen -r discord_voice
```

Nếu có nhiều phiên trùng tên, dùng ID:

```bash
screen -r 12345
```

### Tắt bot đúng cách

Vào lại screen:

```bash
screen -r discord_voice
```

Sau đó trong menu bot chọn:

```text
6. Exit
```

Hoặc nhấn `Ctrl + C`. Sau khi bot dừng, gõ:

```bash
exit
```

để đóng phiên screen.

## Chạy Lại Sau Khi VPS Reboot

Sau khi VPS khởi động lại, vào SSH rồi chạy:

```bash
cd ~/Discord_Voice
screen -S discord_voice
source venv/bin/activate
python3 self-bot.py
```

Nhập channel/mode như bình thường, sau đó detach bằng `Ctrl + A`, rồi `D`.

## Lệnh Nhanh Mỗi Lần Chạy

```bash
cd ~/Discord_Voice
screen -S discord_voice
source venv/bin/activate
python3 self-bot.py
```

Detach:

```text
Ctrl + A, rồi D
```

Vào lại:

```bash
screen -r discord_voice
```

## Xử Lý Lỗi screen

### Báo `There is no screen to be resumed`

Chưa có phiên screen nào đang chạy. Tạo phiên mới:

```bash
screen -S discord_voice
```

### Báo screen đang `Attached`

Phiên screen đang được mở ở một kết nối SSH khác. Ép tách phiên cũ và vào lại:

```bash
screen -d -r discord_voice
```

Hoặc dùng ID:

```bash
screen -d -r 12345
```

### Có quá nhiều phiên screen cũ

Xem danh sách:

```bash
screen -ls
```

Xóa các phiên đã chết:

```bash
screen -wipe
```

Nếu thật sự muốn dừng toàn bộ phiên screen của user hiện tại:

```bash
pkill screen
```

Chỉ dùng `pkill screen` khi bạn chắc chắn không còn chương trình quan trọng nào khác đang chạy trong screen.

## Xử Lý Lỗi Bot

### `File tokens.txt not found`

Bạn đang chạy sai thư mục hoặc chưa tạo `tokens.txt`.

Kiểm tra:

```bash
pwd
ls -l
```

Phải thấy `self-bot.py` và `tokens.txt` trong cùng thư mục.

### `No tokens found`

File `tokens.txt` đang rỗng hoặc sai định dạng. Mở lại:

```bash
nano tokens.txt
```

Mỗi token phải nằm trên một dòng.

### Lỗi thiếu thư viện Python

Kích hoạt venv rồi cài lại:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Lỗi tạo venv trên Ubuntu/Debian

```bash
sudo apt install -y python3-venv python3-pip
python3 -m venv venv
```

### Muốn cài lại môi trường sạch

Chỉ xóa thư mục `venv`, không xóa token:

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Bảo Mật

- Không gửi `tokens.txt` cho người khác.
- Không chụp màn hình có token.
- Không public các file `dead_tokens.txt`, `token_details.csv`, `evs.txt`, `user_info.txt`.
- Nếu nghi token bị lộ, đăng xuất tài khoản Discord trên mọi thiết bị hoặc đổi mật khẩu để token cũ mất hiệu lực.
