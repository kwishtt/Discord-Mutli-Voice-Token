
import discord
import asyncio
import logging
import os
import sys
import csv
import random
from typing import List, Optional
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# -----------------------------------------------------------------------------
# MONKEY PATCH: Fix discord.py-self compatibility with new Discord API
# -----------------------------------------------------------------------------
try:
    import discord
    
    # 1. Helper to safely patch FriendFlags
    def _patched_friend_flags_from_dict(cls, data):
        if data is None:
            return cls.all() # Return all flags true if data is missing
        try:
            return cls(all=data.get('all', True), 
                     mutual_guilds=data.get('mutual_guilds', True), 
                     mutual_friends=data.get('mutual_friends', True))
        except Exception:
            return cls.all()

    # 2. Locate and patch FriendFlags (It can be in enums or flags depending on version)
    TargetFlags = getattr(discord.enums, 'FriendFlags', None)
    if not TargetFlags:
         TargetFlags = getattr(discord.flags, 'FriendFlags', None)

    if TargetFlags:
        TargetFlags._from_dict = classmethod(_patched_friend_flags_from_dict)
        print(Fore.GREEN + "[+] Applied hotfix for start-up crash (FriendFlags).")
    else:
        print(Fore.YELLOW + "[!] Warning: Could not find FriendFlags to patch. Bot might crash on startup.")
        
except Exception as e:
    print(Fore.YELLOW + f"[!] Could not apply hotfix: {e}")

# -----------------------------------------------------------------------------
# LOGGING SETUP
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
# Tắt log nhiễu từ thư viện bên ngoài, chỉ hiện lỗi nghiêm trọng
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('discord.client').setLevel(logging.ERROR)
logging.getLogger('discord.gateway').setLevel(logging.WARNING)
logging.getLogger('discord.http').setLevel(logging.ERROR)
logging.getLogger('websockets').setLevel(logging.ERROR)
logging.getLogger('aiohttp').setLevel(logging.ERROR)

logger = logging.getLogger("MGL_Bot")

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
BANNER = """
 ███╗   ███╗ ██████╗ ██╗
 ████╗ ████║██╔════╝ ██║
 ██╔████╔██║██║  ███╗██║
 ██║╚██╔╝██║██║   ██║██║
 ██║ ╚═╝ ██║╚██████╔╝███████╗
 ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ 
"""

# -----------------------------------------------------------------------------
# CLASS DEFINITIONS
# -----------------------------------------------------------------------------

class VoiceClone(discord.Client):
    """
    Client riêng biệt cho từng token, quản lý việc kết nối Voice.
    """
    def __init__(self, token: str, channel_id: int):
        super().__init__()
        self.token_str: str = token
        self.target_channel_id: int = channel_id
        self.vc: Optional[discord.VoiceClient] = None
        self.is_connected: bool = False
        # Auto-Room tracking: channel mới khi bị server bot move
        self.moved_to_channel: Optional[int] = None
        self.is_leader: bool = False  # Đánh dấu token leader

    async def on_ready(self) -> None:
        """Sự kiện khi bot login thành công."""
        logger.info(Fore.GREEN + f"[+] Logged in: {self.user} ({self.token_str[:6]}...)")
        await self.join_vc()

    # ID duy nhất được phép dùng lệnh chat đồng loạt
    OWNER_ID: int = 1119601947683590145 #TODO 

    async def on_message(self, message):
        """Lắng nghe lệnh chat đặc biệt."""
        # Bỏ qua tin nhắn của chính mình
        if message.author.id == self.user.id:
            return

        # Chỉ cho phép owner sử dụng lệnh chat đồng loạt
        if message.author.id != self.OWNER_ID:
            return

        # Check pattern: <!Nội dung>
        content = message.content.strip()
        if content.startswith("<!") and content.endswith(">"):
            msg_to_say = content[2:-1] # Lấy nội dung bên trong
            
            if msg_to_say:
                try:
                    # Delay ngẫu nhiên để tránh bot spam cùng 1 tích tắc
                    delay = random.uniform(0.5, 2.5) 
                    await asyncio.sleep(delay)
                    
                    # Gửi tin nhắn
                    await message.channel.send(msg_to_say)
                    # logger.info(f"[+] {self.user} echoed: {msg_to_say}") # Optional log
                except Exception as e:
                    pass # Im lặng nếu lỗi (thường là do không có quyền chat)

    async def on_voice_state_update(self, member, before, after) -> None:
        """Theo dõi khi bot bị server bot move sang channel khác (Auto-Room)."""
        # Chỉ quan tâm nếu là leader và bị move
        if not self.is_leader:
            return
        if not self.user or member.id != self.user.id:
            return

        # Detect: trước đó ở lobby, giờ bị move sang channel khác
        if (before.channel and after.channel
                and before.channel.id != after.channel.id
                and before.channel.id == self.target_channel_id):
            new_ch = after.channel
            self.moved_to_channel = new_ch.id
            logger.info(
                Fore.GREEN + f"[*] LEADER {self.user} được move sang room: "
                f"{new_ch.name} ({new_ch.id})"
            )

    async def join_vc(self) -> None:
        """Tham gia vào Voice Channel bằng change_voice_state (Bypass Voice WS handshake)."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                channel = self.get_channel(self.target_channel_id)
                if not channel:
                    # Thử fetch channel nếu không có trong cache (đôi khi cần thiết)
                    try:
                        channel = await self.fetch_channel(self.target_channel_id)
                    except:
                        pass
                
                if not channel:
                    logger.error(Fore.RED + f"[-] Channel ID {self.target_channel_id} not found for {self.user}")
                    return

                if isinstance(channel, discord.VoiceChannel) or isinstance(channel, discord.StageChannel):
                    guild = channel.guild
                    # Join channel dùng change_voice_state (nhẹ hơn, ít lỗi 4006 với selfbot)
                    # Lưu ý: self_video=False mặc định, user có thể bật sau
                    await guild.change_voice_state(channel=channel, self_mute=False, self_deaf=False)
                    
                    # Polling wait for state update (Max 10s)
                    for _ in range(20):
                        await asyncio.sleep(0.5)
                        if guild.me.voice and guild.me.voice.channel and guild.me.voice.channel.id == channel.id:
                            self.is_connected = True
                            logger.info(Fore.CYAN + f"[v] Joined {channel.name} | {self.user}")
                            return # Success
                    
                    logger.warning(Fore.YELLOW + f"[!] Join signal sent but state not updated yet... ({self.user})")
                    # Even if timed out, we don't break immediately, maybe retry or just accept it might update later
                else:
                    logger.warning(Fore.YELLOW + f"[!] ID {self.target_channel_id} is not a Voice Channel.")
                    break
                    
            except Exception as e:
                logger.error(Fore.RED + f"[!] Error joining VC ({self.user}) - Attempt {attempt+1}/{max_retries}: {e}")
                await asyncio.sleep(2)

    async def toggle_state(self, mute: Optional[bool] = None, deaf: Optional[bool] = None, video: Optional[bool] = None) -> None:
        """Bật/tắt trạng thái Mic/Deaf/Video."""
        try:
            # 1. Tìm Channel (Cache -> Fetch)
            channel = self.get_channel(self.target_channel_id)
            if not channel:
                try:
                    channel = await self.fetch_channel(self.target_channel_id)
                except:
                    pass
            
            if not channel:
                logger.warning(f"[!] Channel {self.target_channel_id} not found for {self.user} (Cannot Toggle)")
                return

            guild = channel.guild
            me = guild.me
            
            # 2. Check Voice State
            if not me.voice or not me.voice.channel:
                logger.warning(f"[!] {self.user} is Ready but NOT in Voice (VoiceState is None).")
                return 

            # 3. Apply Changes
            current_voice_state = me.voice
            new_mute = mute if mute is not None else current_voice_state.self_mute
            new_deaf = deaf if deaf is not None else current_voice_state.self_deaf
            new_video = video if video is not None else current_voice_state.self_video

            await guild.change_voice_state(
                channel=me.voice.channel,
                self_mute=new_mute,
                self_deaf=new_deaf,
                self_video=new_video
            )
            logger.info(f"[i] Update {self.user}: Mute={new_mute}, Deaf={new_deaf}, Cam={new_video}")
            
        except Exception as e:
            logger.error(f"[!] Failed to toggle state for {self.user}: {e}")

class BotManager:
    """Class quản lý tập trung các con bot."""
    def __init__(self):
        self.bots: List[VoiceClone] = []
        self.tokens: List[str] = []
        self.channel_ids: List[int] = []  # Hỗ trợ nhiều channel
        self.loop = asyncio.get_event_loop()

    def load_tokens(self, filepath: str = "tokens.txt") -> None:
        """Đọc token từ file."""
        if not os.path.exists(filepath):
            logger.error(Fore.RED + "File tokens.txt not found!")
            sys.exit(1)
            
        with open(filepath, "r") as f:
            lines = f.read().splitlines()
            self.tokens = [line.strip() for line in lines if line.strip()]
        
        logger.info(Fore.YELLOW + f"Loaded {len(self.tokens)} tokens.")

    async def safe_start_bot(self, bot: VoiceClone, token: str) -> None:
        """Wrapper để chạy bot an toàn, bắt lỗi Login."""
        try:
            await bot.start(token)
        except discord.LoginFailure:
            logger.error(Fore.RED + f"[-] Authentication Failed: Token {token[:6]}... is invalid or expired.")
        except Exception as e:
            logger.error(Fore.RED + f"[-] Runtime Error ({token[:6]}...): {e}")
            import traceback
            print(Fore.RED + traceback.format_exc())

    async def start_all(self, delay: float = 5.0) -> None:
        """Khởi động tất cả bot (có delay để tránh rate limit)."""
        tasks = []
        num_channels = len(self.channel_ids)
        
        for i, token in enumerate(self.tokens):
            if len(token) < 5: continue 
            
            # Round-robin: phân chia đều bot vào các channel
            assigned_channel = self.channel_ids[i % num_channels]
            bot = VoiceClone(token, assigned_channel)
            self.bots.append(bot)
            
            logger.info(Fore.BLUE + f"[*] Bot {i+1} → Channel {assigned_channel}")
            
            # Tạo background task an toàn
            asyncio.create_task(self.safe_start_bot(bot, token))
            
            # Delay nhẹ giữa các lần login 
            if i < len(self.tokens) - 1 and delay > 0:
                print(Fore.BLACK + Style.BRIGHT + f"[*] Waiting {delay}s before next login... ({i+1}/{len(self.tokens)})")
                await asyncio.sleep(delay) 

    async def toggle_all(self, mute_toggle: bool = False, cam_toggle: bool = False, deaf_toggle: bool = False) -> None:
        """Hàm helper để toggle state cho toàn bộ bot."""
        ready_bots = [b for b in self.bots if b.is_ready()]
        print(Fore.CYAN + f"[*] Found {len(ready_bots)} ready bots. Executing toggle...")
        
        tasks = []
        for bot in ready_bots:
            tasks.append(bot.toggle_state(mute=mute_toggle, deaf=deaf_toggle, video=cam_toggle))
        
        if tasks:
            await asyncio.gather(*tasks)
            print(Fore.GREEN + "[v] Done executing command.")
        else:
            print(Fore.YELLOW + "[!] No ready bots found.")

    async def spam_reaction(self, channel_id: int, message_id: int, emoji: str) -> None:
        """Cho toàn bộ bot thả reaction vào tin nhắn chỉ định."""
        ready_bots = [b for b in self.bots if b.is_ready()]
        print(Fore.CYAN + f"[*] Found {len(ready_bots)} ready bots. Reacting with {emoji}...")
        
        count = 0
        for bot in ready_bots:
            try:
                # Dùng HTTP request trực tiếp cho lẹ, đỡ phải fetch message
                await bot.http.add_reaction(channel_id, message_id, emoji)
                count += 1
                # Delay nhỏ để tránh spam API quá gắt
                await asyncio.sleep(0.1) 
            except Exception as e:
                logger.error(f"[!] Bot {bot.user} failed to react: {e}")
        
        print(Fore.GREEN + f"[v] Reacted {count}/{len(ready_bots)} times.")

    async def rename_all(self, new_name: str) -> None:
        """Đổi nickname cho toàn bộ bot."""
        ready_bots = [b for b in self.bots if b.is_ready()]
        target_nick = None if new_name.lower() == 'reset' else new_name
        
        print(Fore.CYAN + f"[*] Renaming {len(ready_bots)} bots to '{target_nick if target_nick else '(Default Name)'}'...")
        
        count = 0
        for bot in ready_bots:
            try:
                # Tìm Guild từ Channel ID của bot đó
                channel = bot.get_channel(bot.target_channel_id)
                if not channel:
                    try:
                        channel = await bot.fetch_channel(bot.target_channel_id)
                    except:
                        pass
                
                if channel:
                    # Đổi tên
                    await channel.guild.me.edit(nick=target_nick)
                    logger.info(f"[+] Renamed {bot.user}")
                    count += 1
                else:
                    logger.warning(f"[!] Guild not found for {bot.user}")
                
                # Delay an toàn
                await asyncio.sleep(1.0)
            except Exception as e:
                logger.error(f"[!] Rename failed for {bot.user}: {e}")
        
        print(Fore.GREEN + f"[v] Success: {count}/{len(ready_bots)}")

    async def auto_room_mode(self, lobby_id: int, leader_count: int = 5, delay: float = 5.0) -> None:
        """Chế độ Auto-Room: leader join lobby, đợi move, rồi phân phối còn lại."""
        total = len(self.tokens)
        if total < leader_count:
            print(Fore.RED + f"[!] Cần ít nhất {leader_count} token! Hiện có: {total}")
            return

        # --- Bước 1: Gửi leader vào lobby ---
        print(Fore.YELLOW + f"\n[*] BƯỚC 1: Gửi {leader_count} leader vào lobby {lobby_id}...")
        leaders: List[VoiceClone] = []
        for i in range(leader_count):
            token = self.tokens[i]
            if len(token) < 5:
                continue
            bot = VoiceClone(token, lobby_id)
            bot.is_leader = True  # Đánh dấu leader để track move
            leaders.append(bot)
            self.bots.append(bot)
            logger.info(Fore.BLUE + f"[*] Leader {i+1}/{leader_count} → Lobby {lobby_id}")
            asyncio.create_task(self.safe_start_bot(bot, token))
            if i < leader_count - 1 and delay > 0:
                print(Fore.BLACK + Style.BRIGHT + f"[*] Waiting {delay}s... ({i+1}/{leader_count})")
                await asyncio.sleep(delay)

        # --- Bước 2: Đợi leader được server bot move sang room mới ---
        print(Fore.YELLOW + f"\n[*] BƯỚC 2: Đang đợi server bot tạo room và move leader...")
        print(Fore.BLACK + Style.BRIGHT + "    (Timeout: 3 phút)")

        timeout_seconds: int = 180  # 3 phút
        new_channel_id: Optional[int] = None

        for tick in range(timeout_seconds * 2):  # Check mỗi 0.5s
            await asyncio.sleep(0.5)
            for leader in leaders:
                if leader.moved_to_channel:
                    new_channel_id = leader.moved_to_channel
                    break
            if new_channel_id:
                break
            # Progress mỗi 10s
            if tick > 0 and tick % 20 == 0:
                elapsed = tick // 2
                print(Fore.BLACK + Style.BRIGHT + f"    ... đã đợi {elapsed}s")

        if not new_channel_id:
            print(Fore.RED + "[!] TIMEOUT! Không phát hiện room mới sau 3 phút.")
            print(Fore.RED + "    Đảm bảo server bot có auto-room khi join lobby.")
            return

        print(Fore.GREEN + f"[+] Phát hiện room mới: {new_channel_id}")

        # Đợi thêm 5s để đảm bảo tất cả leader đã được move
        print(Fore.BLACK + Style.BRIGHT + "    Đợi thêm 5s để ổn định...")
        await asyncio.sleep(5)

        # Thu thập tất cả room mới (phòng trường hợp leader bị chia nhiều room)
        new_rooms: List[int] = list(set(
            leader.moved_to_channel for leader in leaders
            if leader.moved_to_channel
        ))
        print(Fore.GREEN + f"[+] Tổng room mới phát hiện: {len(new_rooms)} → {new_rooms}")

        # --- Bước 3: Phân phối token còn lại vào các room mới ---
        remaining_tokens = self.tokens[leader_count:]
        if not remaining_tokens:
            print(Fore.YELLOW + "[!] Không còn token nào để phân phối.")
            return

        num_rooms = len(new_rooms)
        print(Fore.YELLOW + f"\n[*] BƯỚC 3: Phân phối {len(remaining_tokens)} token còn lại vào {num_rooms} room...")

        for i, token in enumerate(remaining_tokens):
            if len(token) < 5:
                continue
            # Round-robin phân phối vào các room
            assigned_room = new_rooms[i % num_rooms]
            bot = VoiceClone(token, assigned_room)
            self.bots.append(bot)
            logger.info(Fore.BLUE + f"[*] Bot {leader_count + i + 1} → Room {assigned_room}")
            asyncio.create_task(self.safe_start_bot(bot, token))
            if i < len(remaining_tokens) - 1 and delay > 0:
                print(Fore.BLACK + Style.BRIGHT + f"[*] Waiting {delay}s... ({leader_count + i + 1}/{total})")
                await asyncio.sleep(delay)

        print(Fore.GREEN + f"\n[+] HOÀN TẤT! Đã phân phối tất cả {total} token.")

    async def shutdown(self) -> None:
        """Đóng tất cả bot."""
        print(Fore.RED + "\n[!] Shutting down all bots...")
        for bot in self.bots:
            await bot.close()

    async def control_loop(self) -> None:
        """Menu điều khiển (Non-blocking)."""
        while True:
            print(Fore.MAGENTA + "\n--- CONTROL MENU ---")
            print("1. Toggle Mic (Mute/Unmute All)")
            print("2. Toggle Cam (On/Off All)")
            print("3. Toggle Deaf (On/Off All)")
            print("4. Spam Reaction (Specific Message)")
            print("5. Rename All Bots (Change Nick)")
            print("6. Exit")
            
            # Chạy input trong executor để không chặn loop
            choice = await self.loop.run_in_executor(None, input, Fore.YELLOW + "Choice: ")
            choice = choice.strip()

            if choice == '1':
                await self.toggle_all(mute_toggle=True)
            elif choice == '2':
                await self.toggle_all(cam_toggle=True)
            elif choice == '3':
                await self.toggle_all(deaf_toggle=True)
            elif choice == '4':
                try:
                    raw = await self.loop.run_in_executor(None, input, "Enter ChannelID MessageID Emoji (space separated): ")
                    parts = raw.strip().split()
                    if len(parts) < 3:
                        print(Fore.RED + "Missing arguments! Format: <ChannelID> <MessageID> <Emoji>")
                        continue
                    cid, mid, emj = int(parts[0]), int(parts[1]), parts[2]
                    asyncio.create_task(self.spam_reaction(cid, mid, emj))
                except ValueError:
                    print(Fore.RED + "Invalid ID format.")
            elif choice == '5':
                new_nick = await self.loop.run_in_executor(None, input, "Enter new nickname (or 'reset'): ")
                asyncio.create_task(self.rename_all(new_nick.strip()))
            elif choice == '6':
                await self.shutdown()
                break
            else:
                print(Fore.RED + "Invalid choice.")


# -----------------------------------------------------------------------------
# MAIN ENTRY
# -----------------------------------------------------------------------------
from colorama import Style

async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.MAGENTA + BANNER)
    
    manager = BotManager()
    manager.load_tokens()

    if not manager.tokens:
        print(Fore.RED + "No tokens found!")
        return

    # --- Chọn chế độ ---
    print(Fore.CYAN + "\nChọn chế độ hoạt động:")
    print(Fore.WHITE + "  1. Normal Mode  - Nhập channel, chia đều bot vào")
    print(Fore.WHITE + "  2. Auto-Room    - 5 leader join lobby → server bot tạo room → phân phối còn lại")
    mode = await asyncio.get_event_loop().run_in_executor(None, input, Fore.YELLOW + "Mode (1/2): ")
    mode = mode.strip()

    # --- Option: Turbo Login ---
    print(Fore.CYAN + "Enable Turbo Login (3s delay) or Safe Mode (8s)? (y/N):")
    turbo_choice = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
    delay_time = 3 if turbo_choice.strip().lower() == 'y' else 8

    if mode == '2':
        # ===== AUTO-ROOM MODE =====
        print(Fore.CYAN + "\n--- AUTO-ROOM MODE ---")
        print(Fore.CYAN + "Nhập Lobby Channel ID (kênh để 5 leader join vào):")
        try:
            lobby_str = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
            lobby_id = int(lobby_str.strip())
        except ValueError:
            print(Fore.RED + "ID không hợp lệ!")
            return

        print(Fore.CYAN + "Số lượng leader (mặc định 5):")
        leader_str = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
        leader_count = 5
        if leader_str.strip().isdigit():
            leader_count = int(leader_str.strip())
            if leader_count < 1:
                leader_count = 5

        print(Fore.GREEN + f"\n[+] Lobby: {lobby_id} | Leader: {leader_count} | Delay: {delay_time}s")
        print(Fore.GREEN + f"[+] Token còn lại ({len(manager.tokens) - leader_count}) sẽ được phân phối sau.")

        # Start auto-room trong background
        asyncio.create_task(manager.auto_room_mode(lobby_id, leader_count, delay_time))

    else:
        # ===== NORMAL MODE =====
        print(Fore.CYAN + "\nEnter Voice Channel IDs (space separated):")
        print(Fore.BLACK + Style.BRIGHT + "VD: 123456789 987654321 555666777")
        try:
            cid_str = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
            channel_ids = [int(cid.strip()) for cid in cid_str.strip().split() if cid.strip()]
            
            if not channel_ids:
                print(Fore.RED + "Không có channel ID nào được nhập!")
                return
            
            manager.channel_ids = channel_ids
            print(Fore.GREEN + f"[+] Đã nhập {len(channel_ids)} channel(s): {channel_ids}")
            
            # Hiển thị phân bổ bot
            print(Fore.YELLOW + f"[*] {len(manager.tokens)} bot sẽ được chia đều vào {len(channel_ids)} channel")
            for i, cid in enumerate(channel_ids):
                bot_count = len([j for j in range(len(manager.tokens)) if j % len(channel_ids) == i])
                print(Fore.BLACK + Style.BRIGHT + f"    Channel {cid}: ~{bot_count} bot")
                
        except ValueError:
            print(Fore.RED + "Invalid ID format. Chỉ nhập số, cách nhau bởi dấu cách.")
            return

        # Start bots in background
        print(Fore.YELLOW + f"[*] Starting bots (Delay: {delay_time}s)...")
        asyncio.create_task(manager.start_all(delay=delay_time))

    # Start control loop (chung cho cả 2 mode)
    try:
        await manager.control_loop()
    except KeyboardInterrupt:
        pass
    finally:
        await manager.shutdown()
        # Wait a bit for connections to close cleanly
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye.")