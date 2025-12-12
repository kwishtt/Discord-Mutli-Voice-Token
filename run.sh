#!/bin/bash

# Màu sắc
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== SMART LAUNCHER V2 (RedHat Optimized) ===${NC}"

# 1. Xác định thư mục
cd "$(dirname "$0")"

# 2. Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[Error] Python3 chưa được cài đặt!${NC}"
    exit 1
fi

# Print version for debug
python3 --version

# 3. Setup Venv
VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}[!] Đang khởi tạo venv mới...${NC}"
    
    # Try standard venv creation with Pip
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[Error] Không thể tạo venv. Vui lòng kiểm tra lại Python installation.${NC}"
        # Fallback suggestion for RedHat/CentOS/Fedora
        echo -e "${YELLOW}Gợi ý: sudo dnf install python3-pip python3-devel${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[v] Venv đã được tạo.${NC}"
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}[*] Đang cài thư viện...${NC}"
        ./$VENV_DIR/bin/pip install --upgrade pip
        ./$VENV_DIR/bin/pip install -r requirements.txt
        
        if [ $? -ne 0 ]; then
             echo -e "${RED}[!] Cài đặt thư viện thất bại.${NC}"
             exit 1
        fi
        echo -e "${GREEN}[v] Cài đặt hoàn tất!${NC}"
    else
        echo -e "${RED}[!] Không tìm thấy requirements.txt${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}[v] Sử dụng venv có sẵn.${NC}"
fi

# 4. Run Bot
echo -e "${GREEN}[*] Đang khởi động Bot...${NC}"
echo "------------------------------------------------"

./$VENV_DIR/bin/python3 self-bot.py

EXIT_CODE=$?

echo "------------------------------------------------"
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}[!] Bot đã dừng với lỗi (Mã: $EXIT_CODE).${NC}"
else
    echo -e "${GREEN}[!] Bot đã dừng.${NC}"
fi

read -p "Ấn Enter để thoát..."
