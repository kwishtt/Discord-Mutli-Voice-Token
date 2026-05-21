import asyncio
import aiohttp
import os
import csv
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

INPUT_FILE = "tokens.txt"
OUTPUT_FILE = "tokens.txt" # Overwrite original
DEAD_FILE = "dead_tokens.txt"
BACKUP_FILE = "tokens.bak"
DETAILS_FILE = "token_details.csv"

CONCURRENCY_LIMIT = 20 # SLOW DOWN to avoid global IP rate limit

async def check_token(session, token, sem):
    async with sem:
        if not token or len(token) < 10:
            return {'token': token, 'valid': False, 'msg': "Format Error"}
            
        headers = {'Authorization': token}
        try:
            async with session.get('https://discord.com/api/v9/users/@me', headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'token': token,
                        'valid': True,
                        'username': f"{data.get('username')}#{data.get('discriminator')}",
                        'email': data.get('email', 'N/A'),
                        'phone': data.get('phone', 'N/A'),
                        'verified': data.get('verified', False),
                        'msg': "OK"
                    }
                elif response.status == 401:
                    return {'token': token, 'valid': False, 'msg': "Unauthorized (Dead)"}
                elif response.status == 403:
                    return {'token': token, 'valid': False, 'msg': "Locked (Phone/Verification)"}
                elif response.status == 429:
                    return {'token': token, 'valid': False, 'msg': "Rate Limited (Skipped)"}
                else:
                    return {'token': token, 'valid': False, 'msg': f"HTTP {response.status}"}
        except Exception as e:
            return {'token': token, 'valid': False, 'msg': str(e)}

async def main():
    if not os.path.exists(INPUT_FILE):
        print(Fore.RED + f"[!] File {INPUT_FILE} not found.")
        return

    # 1. Read and Deduplicate
    print(Fore.CYAN + "[*] Reading and deduplicating tokens...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_tokens = [d.strip() for d in f.read().splitlines() if d.strip()]
    
    unique_tokens = list(set(raw_tokens))
    print(Fore.YELLOW + f"[-] Found {len(raw_tokens)} tokens. Unique: {len(unique_tokens)} (removed {len(raw_tokens) - len(unique_tokens)} duplicates).")

    # Backup
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(raw_tokens))
    print(Fore.BLUE + f"[-] Backup saved to {BACKUP_FILE}")

    # 2. Check Validity
    print(Fore.CYAN + "[*] Checking token liveness and fetching info...")
    valid_details = []
    valid_tokens = []
    dead_tokens = []

    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
    async with aiohttp.ClientSession() as session:
        tasks = [check_token(session, t, sem) for t in unique_tokens]
        
        total = len(tasks)
        done = 0
        
        for future in asyncio.as_completed(tasks):
            result = await future
            done += 1
            
            if result['valid']:
                email_display = result['email'] if result['email'] else "No Email"
                print(Fore.GREEN + f"[{done}/{total}] VALID | {result['username']} | {email_display}")
                valid_tokens.append(result['token'])
                valid_details.append(result)
            else:
                print(Fore.RED + f"[{done}/{total}] DEAD  | {result['msg']} | {result['token'][:10]}...")
                dead_tokens.append(result['token'])

    # 3. Save Results
    print(Fore.CYAN + "\n[*] Saving results...")
    
    # Save clean list
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(valid_tokens))
    
    # Save dead list
    if dead_tokens:
        with open(DEAD_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(dead_tokens))

    # Save details CSV
    if valid_details:
        with open(DETAILS_FILE, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Token", "Username", "Email", "Phone", "Verified"])
            for item in valid_details:
                writer.writerow([
                    item['token'],
                    item['username'],
                    item['email'],
                    item['phone'],
                    str(item['verified'])
                ])
        print(Fore.MAGENTA + f"[+] Statistics saved to {DETAILS_FILE}")

    print(Fore.GREEN + f"\n[DONE] Saved {len(valid_tokens)} valid tokens to {OUTPUT_FILE}.")
    print(Fore.RED + f"[DONE] Removed {len(dead_tokens)} dead tokens.")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
