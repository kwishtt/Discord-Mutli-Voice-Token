# Multi-Token-Voice-24/24

A robust, multi-account Discord self-bot management system designed for 24/7 reliability on Linux/VPS environments.

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

## Project Structure

```text
.
├── docs/                # Documentation
│   ├── GUIDE_VN.md      # Detailed 24/7 VPS setup guide (Vietnamese)
│   └── README_VN.md     # Project overview (Vietnamese)
├── Token Check/         # Utilities for token validation and cleanup
├── self-bot.py          # Main application logic
├── run.sh               # Deployment & environment setup script
├── tokens.txt           # Token list (Git-ignored)
└── requirements.txt     # Python dependencies
```

## Getting Started

### Prerequisites

*   **OS**: Linux (Ubuntu/Debian recommended) or macOS.
*   **Python**: Version 3.8 or higher.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Configure Tokens:**
    Create a file named `tokens.txt` in the root directory and add your discord tokens, one per line.
    ```text
    OTk5...
    MTAw...
    ```

3.  **Setup & Run:**
    The provided script handles virtual environment creation and dependency installation.
    ```bash
    chmod +x run.sh
    ./run.sh
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

---
*Developed by KTMJN Team*
*discord.gg/mgl*