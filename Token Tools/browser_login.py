import os
import time
import sys
import threading

# Check dependencies
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("[-] Missing library! Please install: pip install selenium")
    print("[-] Also ensure you have Chrome/Chromium and 'chromedriver' installed.")
    sys.exit(1)

def login_discord(token):
    print(f"[*] Attempting to login with token prefix: {token[:6]}...")
    
    # Setup Driver (Chrome)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Comment out to see the browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Suppress logging
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"[!] Could not start Chrome Driver: {e}")
        print("[*] Please install chromedriver: sudo apt install chromium-chromedriver (on Debian/Ubuntu)")
        return

    try:
        print("[*] Opening Discord Login Page...")
        driver.get("https://discord.com/login")
        
        # Wait for page load
        time.sleep(3)
        
        print("[*] Injecting Login Script...")
        # The Magic JS
        js_script = f"""
            (function() {{
                let token = "{token}";
                setInterval(() => {{
                    document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"{token}"`
                }}, 50);
                setTimeout(() => {{
                    location.reload();
                }}, 2500);
            }})();
        """
        driver.execute_script(js_script)
        
        print("[v] Script executed. Waiting for reload...")
        time.sleep(5)
        
        current_url = driver.current_url
        if "login" not in current_url:
            print("[+] Login Successful! You are inside.")
        else:
            print("[?] Still on login page. Token might be invalid or 2FA required.")
            
        print("\n[!] Browser is open. Press ENTER in this terminal to close it.")
        input()
        
    except Exception as e:
        print(f"[!] Error during automation: {e}")
    finally:
        print("[*] Closing browser...")
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        # Interactive select from files or manual input
        print("--- DISCORD TOKEN BROWSER LOGIN ---")
        token = input("Enter Token: ").strip()
        
    if token:
        login_discord(token.strip('"'))
