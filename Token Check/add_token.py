import asyncio
import aiohttp
import os
import sys
from colorama import Fore, init

init(autoreset=True)

TOKENS_FILE = "tokens.txt"


async def validate_token(token: str):
    headers = {"Authorization": token}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com/api/v9/users/@me', headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return True, f"{data.get('username')}#{data.get('discriminator', '')}"
                elif resp.status == 401:
                    return False, "Unauthorized (invalid)"
                elif resp.status == 403:
                    return False, "Locked (phone/verification)"
                else:
                    return False, f"HTTP {resp.status}"
    except Exception as e:
        return False, str(e)


def append_token_to_file(token: str) -> bool:
    # Ensure file exists
    if not os.path.exists(TOKENS_FILE):
        open(TOKENS_FILE, 'w', encoding='utf-8').close()

    # Read existing tokens to avoid duplicates
    with open(TOKENS_FILE, 'r', encoding='utf-8') as f:
        existing = [t.strip() for t in f.read().splitlines() if t.strip()]

    if token in existing:
        print(Fore.YELLOW + "[!] Token already present in tokens.txt — skipping append.")
        return False

    # Append token on a new line
    with open(TOKENS_FILE, 'a', encoding='utf-8') as f:
        if existing:
            f.write('\n' + token)
        else:
            f.write(token)

    return True


async def main():
    print("--- Add a token and append to tokens.txt ---")
    token = input("Paste token (or press Enter to cancel): ").strip().strip('"')
    if not token:
        print("Canceled — no token provided.")
        return

    print("[*] Validating token with Discord API...")
    ok, info = await validate_token(token)
    if ok:
        print(Fore.GREEN + f"[+] Valid token: {info}")
        appended = append_token_to_file(token)
        if appended:
            print(Fore.GREEN + "[v] Token appended to tokens.txt")
    else:
        print(Fore.RED + f"[-] Token invalid or error: {info}")
        choice = input("Append anyway? (y/N): ").strip().lower()
        if choice == 'y':
            appended = append_token_to_file(token)
            if appended:
                print(Fore.GREEN + "[v] Token appended to tokens.txt")
            else:
                print(Fore.YELLOW + "[!] Token already present — not appended.")


if __name__ == '__main__':
    if os.name == 'nt':
        # Windows event loop policy for aiohttp
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nCanceled by user.')
