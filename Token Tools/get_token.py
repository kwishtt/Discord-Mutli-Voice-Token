"""
Tool đăng nhập Discord - Lấy Token & User Info
Mở trình duyệt -> Anh đăng nhập thủ công -> Lấy token + user info tự động
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init
import requests
import time
import json
import logging
from datetime import datetime
from typing import Optional

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)

init(autoreset=True)


def timestamp() -> str:
    """Trả về chuỗi timestamp đẹp cho log."""
    return f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M:%S %d-%m-%Y')}]"


def extract_token_from_browser(driver: uc.Chrome) -> Optional[str]:
    """Inject JS vào browser để trích xuất token Discord từ localStorage/webpackChunkdiscord_app."""
    # Script lấy token từ iframe webpack chunk (cách phổ biến nhất, ổn định)
    js_script = """
    return (function() {
        // Cách 1: Lấy từ iframe trick
        var iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        var token = iframe.contentWindow.localStorage.getItem('token');
        document.body.removeChild(iframe);
        if (token) {
            return token.replace(/"/g, '');
        }

        // Cách 2: Lấy trực tiếp từ localStorage
        token = window.localStorage.getItem('token');
        if (token) {
            return token.replace(/"/g, '');
        }

        // Cách 3: Tìm trong webpackChunkdiscord_app
        try {
            var wpRequire;
            window.webpackChunkdiscord_app.push([
                [Math.random()],
                {},
                function(req) { wpRequire = req; }
            ]);
            var mod = Object.values(wpRequire.c).find(
                m => m?.exports?.default?.getToken !== undefined
            );
            if (mod) {
                return mod.exports.default.getToken();
            }
        } catch(e) {}

        return null;
    })();
    """
    try:
        token = driver.execute_script(js_script)
        return token
    except Exception as e:
        logger.error(f"{timestamp()} {Fore.RED}Lỗi khi inject JS lấy token: {e}{Style.RESET_ALL}")
        return None


def fetch_user_info(token: str) -> Optional[dict]:
    """Gọi Discord API /users/@me để lấy thông tin user."""
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    try:
        resp = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        else:
            logger.error(
                f"{timestamp()} {Fore.RED}API trả về status {resp.status_code}: {resp.text}{Style.RESET_ALL}"
            )
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"{timestamp()} {Fore.RED}Lỗi kết nối API: {e}{Style.RESET_ALL}")
        return None


def save_results(token: str, user_info: dict) -> None:
    """Lưu token và thông tin user vào file."""
    username = user_info.get("username", "unknown")
    user_id = user_info.get("id", "unknown")
    email = user_info.get("email", "N/A")
    phone = user_info.get("phone", "N/A")
    discriminator = user_info.get("discriminator", "0")
    global_name = user_info.get("global_name", "N/A")
    mfa_enabled = user_info.get("mfa_enabled", False)
    verified = user_info.get("verified", False)
    nitro_type = user_info.get("premium_type", 0)

    # Lưu token
    with open("tokens.txt", "a", encoding="utf-8") as f:
        f.write(f"{token}\n")

    # Lưu chi tiết vào evs.txt
    info_line = f"{email}:{username}:{user_id}:{token}"
    with open("evs.txt", "a", encoding="utf-8") as f:
        f.write(f"{info_line}\n")

    # Lưu user info đầy đủ vào user_info.txt
    with open("user_info.txt", "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Thoi gian   : {datetime.now().strftime('%H:%M:%S %d-%m-%Y')}\n")
        f.write(f"User ID     : {user_id}\n")
        f.write(f"Username    : {username}\n")
        f.write(f"Global Name : {global_name}\n")
        f.write(f"Discrimin.  : {discriminator}\n")
        f.write(f"Email       : {email}\n")
        f.write(f"Phone       : {phone}\n")
        f.write(f"MFA         : {mfa_enabled}\n")
        f.write(f"Verified    : {verified}\n")
        f.write(f"Nitro Type  : {nitro_type}\n")
        f.write(f"Token       : {token}\n")
        f.write("=" * 60 + "\n\n")

    logger.info(f"{timestamp()} {Fore.GREEN}Da luu token vao tokens.txt{Style.RESET_ALL}")
    logger.info(f"{timestamp()} {Fore.GREEN}Da luu info vao evs.txt & user_info.txt{Style.RESET_ALL}")


def display_user_info(user_info: dict) -> None:
    """In thông tin user ra terminal đẹp."""
    logger.info(f"\n{Fore.CYAN}{'=' * 50}")
    logger.info(f"  THONG TIN TAI KHOAN DISCORD")
    logger.info(f"{'=' * 50}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}User ID     : {Fore.GREEN}{user_info.get('id', 'N/A')}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}Username    : {Fore.GREEN}{user_info.get('username', 'N/A')}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}Global Name : {Fore.GREEN}{user_info.get('global_name', 'N/A')}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}Email       : {Fore.GREEN}{user_info.get('email', 'N/A')}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}Phone       : {Fore.GREEN}{user_info.get('phone', 'N/A')}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}MFA         : {Fore.GREEN}{user_info.get('mfa_enabled', False)}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}Verified    : {Fore.GREEN}{user_info.get('verified', False)}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}Nitro       : {Fore.GREEN}{user_info.get('premium_type', 0)}{Style.RESET_ALL}")
    logger.info(f"  {Fore.WHITE}Locale      : {Fore.GREEN}{user_info.get('locale', 'N/A')}{Style.RESET_ALL}")

    avatar = user_info.get("avatar")
    if avatar:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_info['id']}/{avatar}.png"
        logger.info(f"  {Fore.WHITE}Avatar      : {Fore.BLUE}{avatar_url}{Style.RESET_ALL}")

    logger.info(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")


def main() -> None:
    """Flow chính: mở browser -> đăng nhập -> lấy token -> lấy user info."""
    banner = f"""
{Fore.CYAN}
  ____  _                       _   _                _       
 |  _ \\(_)___  ___ ___  _ __ __| | | |    ___   __ _(_)_ __  
 | | | | / __|/ __/ _ \\| '__/ _` | | |   / _ \\ / _` | | '_ \\ 
 | |_| | \\__ \\ (_| (_) | | | (_| | | |__| (_) | (_| | | | | |
 |____/|_|___/\\___\\___/|_|  \\__,_| |_____\\___/ \\__, |_|_| |_|
                                                |___/         
  Token Grabber - by kwishtt
{Style.RESET_ALL}"""
    logger.info(banner)

    driver: Optional[uc.Chrome] = None
    try:
        logger.info(f"{timestamp()} {Fore.YELLOW}Dang mo trinh duyet...{Style.RESET_ALL}")

        options = uc.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")

        driver = uc.Chrome(
            options=options,
            version_main=148,
            browser_executable_path="/usr/bin/google-chrome"
        )
        driver.maximize_window()


        # Mở trang login Discord
        driver.get("https://discord.com/login")
        logger.info(f"{timestamp()} {Fore.CYAN}Da mo trang dang nhap Discord.{Style.RESET_ALL}")
        logger.info(f"{timestamp()} {Fore.YELLOW}Anh dang nhap thu cong di nha (nhap email/pass hoac quet QR).{Style.RESET_ALL}")

        # Chờ đến khi URL chuyển sang /channels (tức là đã login thành công)
        # Timeout 5 phút cho anh thao tác thoải mái
        try:
            WebDriverWait(driver, 300).until(EC.url_contains("discord.com/channels"))
            logger.info(f"{timestamp()} {Fore.GREEN}Dang nhap thanh cong roi anh!{Style.RESET_ALL}")
        except Exception:
            logger.error(f"{timestamp()} {Fore.RED}Het thoi gian cho dang nhap (5 phut). Thu lai nha anh.{Style.RESET_ALL}")
            return

        # Đợi trang load hoàn toàn
        time.sleep(3)

        # Lấy token từ browser
        logger.info(f"{timestamp()} {Fore.YELLOW}Dang lay token tu browser...{Style.RESET_ALL}")
        token = extract_token_from_browser(driver)

        if not token:
            # Thử lại vài lần
            for attempt in range(3):
                logger.info(f"{timestamp()} {Fore.YELLOW}Thu lai lan {attempt + 1}...{Style.RESET_ALL}")
                time.sleep(2)
                token = extract_token_from_browser(driver)
                if token:
                    break

        if not token:
            logger.error(f"{timestamp()} {Fore.RED}Khong the lay duoc token tu browser. Thu cach khac...{Style.RESET_ALL}")
            # Fallback: yêu cầu anh paste token thủ công
            token = input(f"{timestamp()} {Fore.CYAN}Paste token thu cong vao day (F12 > Console > copy token): {Style.RESET_ALL}").strip()
            if not token:
                logger.error(f"{timestamp()} {Fore.RED}Khong co token. Ket thuc.{Style.RESET_ALL}")
                return

        logger.info(f"{timestamp()} {Fore.GREEN}Lay duoc token: {token[:30]}...{Style.RESET_ALL}")

        # Đóng browser - không cần nữa
        try:
            driver.quit()
            driver = None
        except Exception:
            pass

        # Gọi API lấy user info
        logger.info(f"{timestamp()} {Fore.YELLOW}Dang lay thong tin user tu API...{Style.RESET_ALL}")
        user_info = fetch_user_info(token)

        if user_info:
            # Hiển thị info
            display_user_info(user_info)
            # Lưu file
            save_results(token, user_info)
            logger.info(f"{timestamp()} {Fore.GREEN}Hoan tat! Token va user info da duoc luu.{Style.RESET_ALL}")
        else:
            logger.error(f"{timestamp()} {Fore.RED}Khong lay duoc user info. Chi luu token thoi nha.{Style.RESET_ALL}")
            with open("tokens.txt", "a", encoding="utf-8") as f:
                f.write(f"{token}\n")
            logger.info(f"{timestamp()} {Fore.GREEN}Da luu token vao tokens.txt{Style.RESET_ALL}")

    except KeyboardInterrupt:
        logger.info(f"\n{timestamp()} {Fore.YELLOW}Anh huy roi. Bye bye~{Style.RESET_ALL}")

    except Exception as e:
        logger.error(f"{timestamp()} {Fore.RED}Loi khong mong muon: {e}{Style.RESET_ALL}")

    finally:
        if driver:
            try:
                driver.quit()
                logger.info(f"{timestamp()} {Fore.GREEN}Da dong trinh duyet.{Style.RESET_ALL}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
