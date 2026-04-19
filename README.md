# Multi-Token-Voice-24/24

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-Selfbot-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=for-the-badge&logo=linux&logoColor=black)

![Project Banner](https://i.ibb.co/0ynRbGsM/Music-Soundcloud-Banner.png)

</div>
A robust, multi-account Discord self-bot management system designed for 24/7 reliability on Linux/VPS environments.

## Owner ID (How to set)

Some sensitive global commands are restricted to a single `OWNER_ID`. Set it before running the bot:

1. Open Discord → `User Settings` → `Advanced` → enable **Developer Mode**.
2. Right-click your profile (avatar or name in the member list) → **Copy ID**.
3. Open `self-bot.py` and locate the `OWNER_ID` constant inside the `VoiceClone` class. Replace the placeholder with your numeric ID. Example:

```py
# inside self-bot.py
OWNER_ID: int = 1119601947683590145  # replace this number with your own Discord user ID
```

Save the file and restart the bot.

## Overview

This automated system allows for the scalable deployment and management of multiple Discord user accounts (self-bots) simultaneously. It is engineered with automatic error handling, connection persistence, and resource optimization to ensure uninterrupted voice channel presence.

**For Vietnamese documentation, please see [docs/README_VN.md](docs/README_VN.md).**  
*(Vui lòng xem tài liệu Tiếng Việt tại [docs/README_VN.md](docs/README_VN.md))*

## Core Features

*   **Multi-Instance Architecture**: Seamlessly handles concurrent logins for multiple tokens.
*   **Persistent Voice Connection**: Features "stay-alive" logic to automatically rejoin voice channels upon disconnection or socket errors (Code 4006).
*   **Adaptive Rate-Limiting**:
    *   **Safe Mode**: Sequential login with delays to minimize detection risk.
    *   **Turbo Mode**: High-concurrency login for large-scale deployments.
*   **Centralized Control**: Interactive command-line interface for batch locking mute, deafen, and video states across all instances.
*   **Resource Efficiency**: Optimized for low-memory environments (VPS).

## Windows — Detailed Setup

If you're running this project on Windows, follow these steps for a reliable environment.

1. Install Python 3.8+ from https://www.python.org/ and select "Add Python to PATH" during installer.

2. Open a Command Prompt or PowerShell in the project directory (run as Administrator if you need system-wide installs).

3. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

4. Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. (Optional) If you plan to use `Token Check/browser_login.py` you need Chrome and a matching `chromedriver`:

- Download Chrome/Chromium from Google or Microsoft.
- Download the `chromedriver` version matching your Chrome version and either place it in a folder on your `PATH` or copy the `chromedriver.exe` into the project root.

6. Run the bot (or use `run.bat`):

```powershell
python self-bot.py
# or
.\\run.bat
```

7. Run at startup (optional): use Windows Task Scheduler to create a task that runs on logon and executes `python <full_path>\self-bot.py` with the working directory set to the project folder.

Notes:
- If you need to run multiple instances or services, consider using `nssm` (Non-Sucking Service Manager) to register the script as a Windows service.
- Always keep `tokens.txt` local and never commit it to source control.

## Getting Started

### Prerequisites

*   **OS**: Linux (Ubuntu/Debian recommended) or macOS.
*   **Python**: Version 3.8 or higher.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kwishtt/Discord-Mutli-Voice-Token.git
    cd Discord-Mutli-Voice-Token
    ```

2.  **Configure Tokens:**
    Create a file named `tokens.txt` in the root directory and add your discord tokens, one per line.
    ```text
    OTk5...
    MTAw...
    ```

3.  **Setup & Run:**

    *   **Linux / macOS:**
        ```bash
        chmod +x run.sh
        ./run.sh
        ```
    
    *   **Windows:**
        Double-click `run.bat` or run in CMD:
        ```cmd
        run.bat
        ```

### Manual Installation (If scripts fail)

If you prefer to set up the environment manually or encounter issues with the automatic scripts:

**Linux / macOS:**
```bash
# 1. Create Virtual Environment
python3 -m venv venv

# 2. Activate Venv
source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run the Bot
python3 self-bot.py
```

**Windows:**
```cmd
:: 1. Create Virtual Environment
python -m venv venv

:: 2. Activate Venv
venv\Scripts\activate

:: 3. Install Dependencies
pip install -r requirements.txt

:: 4. Run the Bot
python self-bot.py
```

## Usage

Upon launching `self-bot.py`, follow the interactive prompts:

1.  **Channel Input**: Enter the numeric ID(s) of the target voice channel(s).
2.  **Mode Selection**: Choose `1` for Safe Mode (recommended) or `2` for Turbo Mode.
3.  **Runtime Control**: Use the displayed dashboard to toggle states:
    *   `[1]` Toggle Mute
    *   `[2]` Toggle Deafen
    *   `[3]` Toggle Camera

## Disclaimer

This software is designed for educational and management purposes. Using self-bots (automating user accounts) may violate Discord's Terms of Service. The developers are not responsible for any account suspensions or bans resulting from the use of this tool. Use at your own risk.

## Token Check utilities

Two helper scripts live in the `Token Check/` folder to help validate and prepare token lists safely:

- `Token Check/browser_login.py`
    - Purpose: Use a Chrome webdriver to inject a token into a browser session and attempt a login. Helpful to quickly verify a token in a browser environment.
    - Usage (interactive):
        ```bash
        python "Token Check/browser_login.py"
        # or pass token directly
        python "Token Check/browser_login.py" "YOUR_TOKEN_HERE"
        ```
    - Requirements: `selenium`, a compatible `chromedriver`, and Chrome/Chromium installed.
    - Notes: This script opens a real browser window (headless mode is commented out by default). Close the browser when finished.
    
- `Token Check/cleaner.py`
    - Purpose: Read `tokens.txt`, deduplicate entries, check token validity using the Discord API, and overwrite `tokens.txt` with only valid tokens. Generates `dead_tokens.txt`, `tokens.bak` (backup), and `token_details.csv` (info about valid tokens).
    - Usage:
        ```bash
        pip install -r requirements.txt  # ensure aiohttp and dependencies are installed
        python "Token Check/cleaner.py"
        ```
    - Output files created/updated:
        - `tokens.txt` (overwritten with valid tokens)
        - `dead_tokens.txt` (invalid/dead tokens)
        - `tokens.bak` (original backup)
        - `token_details.csv` (username/email/verified information for valid tokens)

Security reminder: Never commit `tokens.txt`, `dead_tokens.txt`, or other token-containing files to a public repository. The repo's `.gitignore` now includes `*.txt` to help prevent accidental commits, but double-check before pushing.

### New: `Token Check/add_token.py`

 - Purpose: Interactive helper to paste a token, validate it against the Discord API, and append it to `tokens.txt` (appends to the end — does not overwrite).
 - Usage:
     ```bash
     pip install -r requirements.txt  # ensure aiohttp and colorama are installed
     python "Token Check/add_token.py"
     ```
 - Behavior: The script validates the token; if valid it is appended to `tokens.txt` unless already present. If invalid, the script asks whether to append anyway.

## Support Me 

*   **⭐ Star Project**: Star this project on GitHub to show your support!
*   **Discord**: Join the support server [discord.gg/mgl](https://discord.gg/mgl)
---
*Developed by kwishtt*
