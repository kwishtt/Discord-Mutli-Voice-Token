# Multi-Token Voice 24/7

A Discord multi-account voice launcher for keeping many accounts connected to voice channels from one terminal. It supports Windows, macOS, Linux, and VPS usage.

> Vietnamese documentation: [docs/README_VN.md](docs/README_VN.md)
> 24/7 VPS guide: [docs/GUIDE_VN.md](docs/GUIDE_VN.md)

## Important Notice

This project uses Discord user tokens and self-bot behavior. Automating user accounts may violate Discord's Terms of Service and may lead to account restrictions. Use it only if you understand the risk. Keep token files private and never upload them to a public repository.

## What This Tool Does

- Logs in multiple Discord tokens from `tokens.txt`.
- Joins one or more voice channel IDs.
- Splits tokens evenly across multiple channels in Normal Mode.
- Supports Auto-Room mode for lobby based room creation workflows.
- Provides a terminal menu to toggle mic, camera, deaf, spam reaction, rename, or exit.
- Reconnects and keeps voice sessions alive as much as possible.

## Project Files

```text
.
├── self-bot.py                  # Main bot program
├── run.bat                      # Windows launcher
├── run.sh                       # macOS/Linux launcher
├── requirements.txt             # Python dependencies
├── tokens.txt                   # Your tokens, one per line
├── docs/
│   ├── README_VN.md             # Vietnamese setup guide
│   └── GUIDE_VN.md              # 24/7 VPS/screen guide
└── Token Tools/
    ├── get_token.py             # Browser login and token/user-info helper
    ├── check_info_token.py      # Validate tokens and export token info
    └── browser_login.py         # Test login with a token in Chrome
```

## Requirements

- Python 3.8 or newer.
- Git, if you clone the project from GitHub.
- Chrome/Chromium only if you use scripts inside `Token Tools/`.

Check Python:

```bash
python --version
python3 --version
```

On Windows, `python` is usually correct. On macOS/Linux, `python3` is usually correct.

## Step 1: Prepare Tokens

Create `tokens.txt` in the project root, beside `self-bot.py`.

```text
TOKEN_1
TOKEN_2
TOKEN_3
```

Rules:

- Put one token per line.
- Do not add quotes.
- Do not share this file.
- Do not commit this file.

## Step 2: Set OWNER_ID

Some sensitive commands are restricted to one Discord user ID.

1. Open Discord.
2. Go to `User Settings` -> `Advanced`.
3. Enable `Developer Mode`.
4. Right-click your Discord profile and choose `Copy ID`.
5. Open `self-bot.py`.
6. Find this line inside `VoiceClone`:

```py
OWNER_ID: int = 1119601947683590145
```

Replace the number with your own Discord user ID, save the file, then restart the bot.

## Quick Start

### Windows

Double-click `run.bat`, or run:

```cmd
run.bat
```

The launcher creates `venv`, installs dependencies, and starts `self-bot.py`.

### macOS / Linux

Run:

```bash
chmod +x run.sh
./run.sh
```

The launcher creates `venv`, installs dependencies, and starts `self-bot.py`.

## Manual Setup

Use this if the launcher fails or if you prefer running commands yourself.

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

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then open PowerShell again and retry the activation command.

### macOS

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 self-bot.py
```

If `python3 -m venv` fails, install Python from https://www.python.org/ or Homebrew.

### Linux / VPS

Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 self-bot.py
```

Fedora/CentOS/RHEL:

```bash
sudo dnf install -y python3 python3-pip python3-devel
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 self-bot.py
```

## How To Run

After the program starts:

1. Choose mode:
   - `1` Normal Mode: enter voice channel IDs manually.
   - `2` Auto-Room: send leader tokens into a lobby, then distribute remaining tokens after rooms are created.
2. Choose login speed:
   - `N` or Enter: Safe Mode, 8 second delay.
   - `y`: Turbo Mode, 3 second delay.
3. Enter channel IDs:
   - One channel: `123456789012345678`
   - Multiple channels: `123456789012345678 987654321098765432`
4. Use the control menu:
   - `1` Toggle mic for all accounts.
   - `2` Toggle camera for all accounts.
   - `3` Toggle deaf for all accounts.
   - `4` Spam reaction on a message.
   - `5` Rename all accounts in the server.
   - `6` Exit.

## Running 24/7 On VPS

For a VPS, use `screen` so the bot keeps running after you disconnect SSH:

```bash
screen -S discord_voice
source venv/bin/activate
python3 self-bot.py
```

Detach without stopping:

```text
Ctrl + A, then D
```

Return later:

```bash
screen -r discord_voice
```

Full Vietnamese VPS guide: [docs/GUIDE_VN.md](docs/GUIDE_VN.md)

## Token Tools

Install dependencies first:

```bash
pip install -r requirements.txt
```

Validate tokens and write token details:

```bash
python "Token Tools/check_info_token.py"
```

Open Chrome and test login with a token:

```bash
python "Token Tools/browser_login.py"
python "Token Tools/browser_login.py" "YOUR_TOKEN_HERE"
```

Open Chrome, log in manually, and save token/user info:

```bash
python "Token Tools/get_token.py"
```

Notes:

- `get_token.py` is currently configured for Linux Chrome at `/usr/bin/google-chrome`.
- Browser tools require Chrome/Chromium and compatible driver support.
- Generated files such as `tokens.txt`, `dead_tokens.txt`, `token_details.csv`, `evs.txt`, and `user_info.txt` may contain sensitive data.

## Common Problems

### `File tokens.txt not found`

Create `tokens.txt` in the same folder as `self-bot.py`.

### `No tokens found`

Make sure `tokens.txt` has at least one non-empty line.

### `python` is not recognized on Windows

Reinstall Python and enable `Add Python to PATH`, then reopen CMD/PowerShell.

### `python3 -m venv` fails on Ubuntu/Debian

Install venv support:

```bash
sudo apt install -y python3-venv python3-pip
```

### PowerShell cannot activate venv

Run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Chrome driver error in Token Tools

Install Chrome/Chromium and make sure Selenium can start Chrome. On Debian/Ubuntu:

```bash
sudo apt install -y chromium chromium-driver
```

## Support

- Star the project on GitHub if it helps you.
- Discord support server: https://discord.gg/mgl

Developed by `kwishtt`.
