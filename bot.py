import os
import time
import logging
import asyncio
import aiohttp
import subprocess
import random
import youtube
from datetime import datetime, timedelta
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant
import yt_dlp
from aiohttp import web

# Logging Setup
logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Channel IDs
DATABASE_CHANNEL_ID = int(os.environ.get("DATABASE_CHANNEL_ID", "-1004396122384"))
LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", "-1004441596603"))
ALLOWED_GROUP_ID = int(os.environ.get("ALLOWED_GROUP_ID", "0"))

ADMIN_ID = 1727225499

# Force Subscribe Channels
F_SUB_CHANNEL_1 = os.environ.get("F_SUB_CHANNEL_1", "AlluTvSerials")
F_SUB_CHANNEL_2 = os.environ.get("F_SUB_CHANNEL_2", "leech_Update_Channel")

# Start & Command Reactions
REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"]

async def send_random_reaction(client, message):
    """Sends a random reaction to user messages"""
    try:
        reaction = random.choice(REACTIONS)
        await client.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.id,
            reaction=reaction
        )
    except Exception as e:
        logging.error(f"Failed to set reaction: {e}")

# Premium, Referral & Payment Variables
REFERAL_COUNT = int(os.environ.get('REFERAL_COUNT', '20'))
REFERAL_PREMEIUM_TIME = os.environ.get('REFERAL_PREMEIUM_TIME', '1month')
PAYMENT_QR = os.environ.get('PAYMENT_QR', 'https://ibb.co/xtr2Bb71')
PAYMENT_TEXT = os.environ.get('PAYMENT_TEXT', '<b>- ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs ❤️ - \n- 15ʀs - 1 ᴅᴀʏꜱ\n- 40ʀs - 1 ᴡᴇᴇᴋ\n- 89ʀs - 1 ᴍᴏɴᴛʜs\n\n🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs 🎁\n\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ\n○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs\n○ ᴜɴʟ𝙸ᴍ𝙸ᴛᴇD ᴍᴏᴠɪᴇs & sᴇʀɪᴇs\n○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n○ ʀᴇǫᴜᴇsْت ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 1ʜ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ\n\n✨ ᴜᴘɪ ɪᴅ - <code>vijayalakshmik8825@ybl</code>\n\nᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ /myplan\n\n💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ\n\n‼️ ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ yᴏU ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ</b>')
OWNER_USERNAME = os.environ.get('OWNER_USERNAME', 'Anujith1238')

# Token Verification Info :
VERIFY = bool(os.environ.get('VERIFY', True))
VERIFY_SHORTLINK_URL = os.environ.get('VERIFY_SHORTLINK_URL', 'linkshortify.com')
VERIFY_SHORTLINK_API = os.environ.get('VERIFY_SHORTLINK_API', '927f420bfcbeda36287288f7e98110467feedbef')
VERIFY_TUTORIAL = os.environ.get('VERIFY_TUTORIAL', 'https://t.me/How_or_Open_Link')

app = Client("LeechBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

USER_THUMBNAILS = {}
WAITING_FOR_THUMB = set()
USER_YTDL_LINKS = {}
USER_FILE_MODES = {}
USER_STATES = {}
RENAME_DATA = {}

ACTIVE_TASKS = {}
USER_TASK_LIMIT = 2
CANCEL_REQUESTS = set()

PREMIUM_USERS = {}
VERIFIED_USERS = {}

START_IMAGE_URL = "https://files.catbox.moe/yazhfx.jpg"

async def web_handler(request):
    return web.Response(text="Bot is Live! 🚀")

async def start_web_server():
    web_app = web.Application()
    web_app.add_routes([web.get("/", web_handler)])
    runner = web.AppRunner(web_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")

def human_bytes(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"

def is_premium(user_id):
    if user_id == ADMIN_ID:
        return True
    if user_id in PREMIUM_USERS:
        if time.time() < PREMIUM_USERS[user_id]:
            return True
        else:
            del PREMIUM_USERS[user_id]
    return False

def is_verified(user_id):
    if is_premium(user_id):
        return True
    if not VERIFY:
        return True
    if user_id in VERIFIED_USERS:
        if time.time() < VERIFIED_USERS[user_id]:
            return True
        else:
            del VERIFIED_USERS[user_id]
    return False

async def get_shortlink(url):
    api_url = f"https://{VERIFY_SHORTLINK_URL}/api?api={VERIFY_SHORTLINK_API}&url={url}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=10) as response:
                data = await response.json()
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    except Exception as e:
        logging.error(f"Error fetching shortlink: {e}")
    return url

async def verification_keyboard(client, user_id):
    bot_info = await client.get_me()
    bot_username = bot_info.username
    long_url = f"https://t.me/{bot_username}?start=verify_{user_id}"
    short_url = await get_shortlink(long_url)
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Click Here to Verify", url=short_url)],
        [InlineKeyboardButton("❓ How to Open Link", url=VERIFY_TUTORIAL)]
    ])

async def check_fsub(client, user_id):
    if user_id == ADMIN_ID:
        return True
    
    channels = [F_SUB_CHANNEL_1, F_SUB_CHANNEL_2]
    for channel in channels:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            return False
        except Exception:
            try:
                ch = channel if channel.startswith("@") else f"@{channel}"
                await client.get_chat_member(ch, user_id)
            except Exception:
                pass
    return True

async def not_joined_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Update Channel 1", url="https://t.me/AlluTvSerials")],
        [InlineKeyboardButton("📢 Join Update Channel 2", url="https://t.me/leech_Update_Channel")],
        [InlineKeyboardButton("🔄 Try Again", callback_data="check_fsub")]
    ])

def get_video_info(file_path):
    duration = 0
    width = 0
    height = 0
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "format=duration:stream=width,height",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) >= 3:
            width = int(lines[0]) if lines[0].isdigit() else 0
            height = int(lines[1]) if lines[1].isdigit() else 0
            duration = int(float(lines[2])) if lines[2] else 0
    except Exception as e:
        logging.error(f"Error getting video info: {e}")
    return duration, width, height

def generate_thumbnail(video_path, user_id):
    os.makedirs("thumbnails", exist_ok=True)
    thumb_path = f"thumbnails/auto_{user_id}.jpg"
    try:
        cmd = [
            "ffmpeg", "-ss", "00:00:05", "-i", video_path,
            "-vframes", "1", "-q:v", "2", thumb_path, "-y"
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
            return thumb_path
    except Exception as e:
        logging.error(f"Error generating thumbnail: {e}")
    return None

def get_progress_bar(percentage):
    completed = int(percentage / 10)
    remaining = 10 - completed
    return "█" * completed + "░" * remaining

async def download_thumbnail_from_source(client, thumb_source, user_id):
    os.makedirs("thumbnails", exist_ok=True)
    custom_thumb_path = f"thumbnails/custom_{user_id}.jpg"
    try:
        if "t.me/" in thumb_source:
            parts = thumb_source.strip("/").split("/")
            msg_id = int(parts[-1])
            channel_username = parts[-2]
            target_msg = await client.get_messages(channel_username, msg_id)
            if target_msg and target_msg.media:
                downloaded_thumb = await client.download_media(target_msg, file_name=custom_thumb_path)
                if downloaded_thumb and os.path.exists(downloaded_thumb):
                    return downloaded_thumb
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(thumb_source) as resp:
                    if resp.status == 200:
                        with open(custom_thumb_path, "wb") as f:
                            f.write(await resp.read())
                        if os.path.exists(custom_thumb_path) and os.path.getsize(custom_thumb_path) > 0:
                            return custom_thumb_path
    except Exception as e:
        logging.error(f"Failed to fetch custom thumbnail from -t: {e}")
    return None

@app.on_message(filters.command("addpremium") & (filters.private | filters.chat(ALLOWED_GROUP_ID)))
async def add_premium_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    if message.from_user.id != ADMIN_ID:
        await message.reply_text("❌ You are not authorized to use this command!")
        return

    if len(message.command) < 3:
        await message.reply_text("❌ Usage: `/addpremium <user_id> <days>`")
        return

    try:
        target_user_id = int(message.command[1])
        days = int(message.command[2])
        expiry_time = time.time() + (days * 24 * 60 * 60)
        PREMIUM_USERS[target_user_id] = expiry_time
        await message.reply_text(f"✅ Successfully added user `{target_user_id}` to Premium for `{days}` days!")
    except Exception as e:
        await message.reply_text(f"❌ Failed to add premium! Error: `{str(e)}`")

@app.on_message(filters.command("removepremium") & (filters.private | filters.chat(ALLOWED_GROUP_ID)))
async def remove_premium_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    if message.from_user.id != ADMIN_ID:
        await message.reply_text("❌ You are not authorized to use this command!")
        return

    if len(message.command) < 2:
        await message.reply_text("❌ Usage: `/removepremium <user_id>`")
        return

    try:
        target_user_id = int(message.command[1])
        if target_user_id in PREMIUM_USERS:
            del PREMIUM_USERS[target_user_id]
            await message.reply_text(f"✅ Successfully removed user `{target_user_id}` from Premium!")
        else:
            await message.reply_text("⚠️ This user is not in the premium list.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to remove premium! Error: `{str(e)}`")

@app.on_message((filters.command("plan") | filters.command("plans")) & (filters.private | filters.chat(ALLOWED_GROUP_ID)))
async def plan_command_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    user_id = message.from_user.id
    if not await check_fsub(client, user_id):
        await message.reply_text(
            "⚠️ **Force Subscription Required!**\n\n"
            "You must join our update channels below to view plans.",
            reply_markup=await not_joined_keyboard()
        )
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Contact Admin", url=f"https://t.me/{OWNER_USERNAME}")]
    ])
    try:
        await message.reply_photo(
            photo=PAYMENT_QR,
            caption=PAYMENT_TEXT,
            reply_markup=keyboard
        )
    except Exception:
        await message.reply_text(
            PAYMENT_TEXT,
            reply_markup=keyboard
        )

@app.on_message(filters.command("myplan") & (filters.private | filters.chat(ALLOWED_GROUP_ID)))
async def myplan_command_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    user_id = message.from_user.id
    if not await check_fsub(client, user_id):
        await message.reply_text(
            "⚠️ **Force Subscription Required!**\n\n"
            "You must join our update channels below to check your plan.",
            reply_markup=await not_joined_keyboard()
        )
        return

    user_name = message.from_user.first_name

    if is_premium(user_id):
        if user_id == ADMIN_ID:
            status_text = "👑 **Status:** Admin / Lifetime Premium ♾️"
        else:
            expiry_timestamp = PREMIUM_USERS.get(user_id, time.time())
            expiry_date = datetime.fromtimestamp(expiry_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            status_text = f"🌟 **Status:** Active Premium User ✨\n⏳ **Expires On:** `{expiry_date}`"
    else:
        status_text = "📦 **Status:** Free User / Standard Plan\n\n💡 *Upgrade to Premium to get unlimited downloads and ad-free experience! Use /plan to check details.*"

    await message.reply_text(
        f"👤 **User Account Plan Info:**\n\n"
        f"<b>Name:</b> {user_name}\n"
        f"<b>User ID:</b> <code>{user_id}</code>\n\n"
        f"{status_text}"
    )

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    user = message.from_user
    user_id = user.id if user else 0

    if len(message.command) > 1 and message.command[1].startswith("verify_"):
        try:
            target_id = int(message.command[1].split("_")[1])
            if target_id == user_id:
                VERIFIED_USERS[user_id] = time.time() + (12 * 60 * 60)
                await message.reply_text(
                    "🎉 **Verification Successful!** ✅\n\n"
                    "Your token verification has been completed successfully. "
                    "You now have unlimited download access for the next **12 Hours**! 🚀"
                )
                return
        except Exception:
            pass

    if not await check_fsub(client, user_id):
        await message.reply_text(
            "⚠️ **Force Subscription Required!**\n\n"
            "You must join our update channels below to use this bot.\n\n"
            "👉 **Join Update Channel 1 & 2, then click Try Again!**",
            reply_markup=await not_joined_keyboard()
        )
        return

    user_name = user.first_name if user else "Unknown"
    username = f"@{user.username}" if user and user.username else "No Username"

    if user and not user.is_bot:
        log_msg = (
            f"👤 <b>New User Started Bot!</b>\n\n"
            f"<b>Name:</b> {user_name}\n"
            f"<b>User ID:</b> <code>{user_id}</code>\n"
            f"<b>Username:</b> {username}"
        )
        try:
            await client.send_message(chat_id=LOG_CHANNEL_ID, text=log_msg)
        except Exception as e:
            logging.error(f"Failed to send start log to LOG_CHANNEL: {e}")

    welcome_text = (
        f"🌟 **Welcome to Advanced Leech Bot, {user_name}!** 🚀\n\n"
        f"I am an advanced Leech Bot. I can help you download videos and audio from TeraBox, YouTube, Gofile, Telegram links, M3U8, MP4, MP3, and more.\n\n"
        f"🛠️ **Key Features:**\n"
        f" • Use `-n` to rename media.\n"
        f" • Use `-t` to set custom thumbnails.\n"
        f" • Use `/usetting` to configure settings.\n"
        f" • Premium users get unlimited concurrent tasks!\n\n"
        f"For any assistance or support, feel free to contact the admin below. 👇"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Contact Admin", url=f"https://t.me/{OWNER_USERNAME}")]
    ])
    
    try:
        await message.reply_photo(
            photo=START_IMAGE_URL,
            caption=welcome_text,
            reply_markup=keyboard
        )
    except Exception:
        await message.reply_text(
            welcome_text,
            reply_markup=keyboard
        )

@app.on_message(filters.command("help") & (filters.private | filters.chat(ALLOWED_GROUP_ID)))
async def help_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    user_id = message.from_user.id
    if not await check_fsub(client, user_id):
        await message.reply_text(
            "⚠️ **Force Subscription Required!**\n\n"
            "You must join our update channels below to access help.",
            reply_markup=await not_joined_keyboard()
        )
        return

    help_text = (
        "🆘 **Need Help & Support?** 🛠️\n\n"
        "Dear user, if you are facing any issues with downloads or have any questions regarding the bot's functionality, we are here to help you!\n\n"
        "You can directly contact our admin for support using the button below. 👇"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Contact Admin", url=f"https://t.me/{OWNER_USERNAME}")]
    ])

    await message.reply_text(
        help_text,
        reply_markup=keyboard
    )

@app.on_message(filters.command("usetting") & (filters.private | filters.chat(ALLOWED_GROUP_ID)))
async def usetting_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    user_id = message.from_user.id
    if not await check_fsub(client, user_id):
        await message.reply_text(
            "⚠️ **Force Subscription Required!**\n\n"
            "You must join our update channels below to use settings.",
            reply_markup=await not_joined_keyboard()
        )
        return

    has_thumb = "Yes 🖼️" if user_id in USER_THUMBNAILS and USER_THUMBNAILS[user_id] else "No ❌"
    current_mode = USER_FILE_MODES.get(user_id, "video")
    mode_text = "📹 Video Format" if current_mode == "video" else "📁 Document Format"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Thumbnail Set: {has_thumb}", callback_data="set_thumb")],
        [InlineKeyboardButton(f"Mode: {mode_text}", callback_data="toggle_mode")],
        [InlineKeyboardButton("👁️ View Thumbnail", callback_data="view_thumb")],
        [InlineKeyboardButton("🗑️ Remove Thumbnail", callback_data="remove_thumb")]
    ])
    
    await message.reply_text(
        "⚙️ **User Personal Settings**\n\n"
        "Configure your personal thumbnail, view it, or change upload format here:",
        reply_markup=keyboard
    )

@app.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if data == "check_fsub":
        if await check_fsub(client, user_id):
            await callback_query.message.edit_text("✅ Thank you for joining our update channels! You can now use the bot freely. Send /start or your command again.")
        else:
            await callback_query.answer("❌ You have not joined both update channels yet! Please join them first.", show_alert=True)
        return

    if not await check_fsub(client, user_id):
        await callback_query.message.edit_text(
            "⚠️ **Force Subscription Required!**\n\n"
            "You must join our update channels below to proceed.",
            reply_markup=await not_joined_keyboard()
        )
        return

    if data == "set_thumb":
        WAITING_FOR_THUMB.add(user_id)
        await callback_query.message.edit_text(
            "🖼️ Please send your thumbnail photo (Image) here.\n"
            "The bot will automatically save it as your default thumbnail!"
        )
    elif data == "view_thumb":
        if user_id in USER_THUMBNAILS and USER_THUMBNAILS[user_id] and os.path.exists(USER_THUMBNAILS[user_id]):
            await client.send_photo(
                chat_id=callback_query.message.chat.id,
                photo=USER_THUMBNAILS[user_id],
                caption="🖼️ **Your Current Saved Thumbnail:**"
            )
            await callback_query.answer("Here is your thumbnail!")
        else:
            await callback_query.answer("❌ You haven't set any custom thumbnail yet!", show_alert=True)

    elif data == "remove_thumb":
        if user_id in USER_THUMBNAILS:
            if USER_THUMBNAILS[user_id] and os.path.exists(USER_THUMBNAILS[user_id]):
                try:
                    os.remove(USER_THUMBNAILS[user_id])
                except:
                    pass
            del USER_THUMBNAILS[user_id]
        if user_id in WAITING_FOR_THUMB:
            WAITING_FOR_THUMB.remove(user_id)
            
        await callback_query.message.edit_text("🗑️ Your thumbnail has been successfully removed!")
    
    elif data == "toggle_mode":
        current_mode = USER_FILE_MODES.get(user_id, "video")
        new_mode = "document" if current_mode == "video" else "video"
        USER_FILE_MODES[user_id] = new_mode
        mode_text = "📹 Video Format" if new_mode == "video" else "📁 Document Format"
        
        has_thumb = "Yes 🖼️" if user_id in USER_THUMBNAILS and USER_THUMBNAILS[user_id] else "No ❌"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"Thumbnail Set: {has_thumb}", callback_data="set_thumb")],
            [InlineKeyboardButton(f"Mode: {mode_text}", callback_data="toggle_mode")],
            [InlineKeyboardButton("👁️ View Thumbnail", callback_data="view_thumb")],
            [InlineKeyboardButton("🗑️ Remove Thumbnail", callback_data="remove_thumb")]
        ])
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        await callback_query.answer(f"Changed upload mode to {new_mode}!")

    elif data.startswith("cancel_dl_"):
        parts = data.split("_")
        task_user_id = int(parts[2])
        if user_id == task_user_id or user_id == ADMIN_ID:
            CANCEL_REQUESTS.add(task_user_id)
            await callback_query.answer("⚠️ Task Cancel requested... Please wait.", show_alert=True)
        else:
            await callback_query.answer("❌ You are not authorized to cancel this task!", show_alert=True)

    elif data == "start_rename":
        USER_STATES[user_id] = "waiting_for_name"
        RENAME_DATA[user_id] = {"original_msg": callback_query.message.reply_to_message}
        await callback_query.message.edit_text(
            "Please send the new name you want to give.\n"
            "Examples: `New_Movie.mp4`, `New_Song.mp3`, `Movie.mkv`"
        )
        await callback_query.answer()

    elif data.startswith("rename_mode_"):
        mode = data.split("_")[2] # video or document
        data_info = RENAME_DATA.get(user_id)
        if not data_info:
            await callback_query.message.edit_text("❌ Session expired. Please try again.")
            return

        original_msg = data_info.get("original_msg")
        new_name = data_info.get("new_name")

        try:
            await callback_query.message.delete()
        except Exception:
            pass

        status_msg = await callback_query.message.reply_text(f"⏳ Processing renamed file as `{mode}`... Please wait.")
        await process_renamed_file(client, status_msg, user_id, callback_query.from_user.first_name, original_msg, new_name, mode)
        
        if user_id in RENAME_DATA:
            del RENAME_DATA[user_id]

    elif data.startswith("ytdl_"):
        format_code = data.split("_")[1]
        url = USER_YTDL_LINKS.get(user_id)
        if not url:
            await callback_query.message.edit_text("❌ Link expired or not found. Please send the `/ytdl` command again.")
            return

        if not is_verified(user_id):
            keyboard = await verification_keyboard(client, user_id)
            await callback_query.message.edit_text(
                "⚠️ **Token Verification Required!**\n\n"
                "You haven't verified your token for the last 12 hours. Please click the button below to verify and unlock downloads.",
                reply_markup=keyboard
            )
            return

        if not is_premium(user_id):
            active_count = ACTIVE_TASKS.get(user_id, 0)
            if active_count >= USER_TASK_LIMIT:
                await callback_query.message.edit_text(
                    f"⚠️ **Limit Exceeded!**\n\n"
                    f"You have `{active_count}` active downloads running. "
                    f"Upgrade to Premium for unlimited downloads!"
                )
                return

        await callback_query.message.edit_text("⏳ Initializing download with selected quality... Please wait.")
        await process_download(client, callback_query.message, user_id, callback_query.from_user.first_name, url, None, None, format_code)

@app.on_message(filters.photo & (filters.private | filters.chat(ALLOWED_GROUP_ID)))
async def save_thumbnail(client: Client, message: Message):
    user_id = message.from_user.id
    if not await check_fsub(client, user_id):
        return

    if user_id in WAITING_FOR_THUMB:
        os.makedirs("thumbnails", exist_ok=True)
        photo_path = f"thumbnails/{user_id}.jpg"
        await message.download(file_name=photo_path)
        USER_THUMBNAILS[user_id] = photo_path
        WAITING_FOR_THUMB.remove(user_id)
        await message.reply_text("✅ Thumbnail saved successfully!")

@app.on_message(filters.command("leech") & filters.chat(ALLOWED_GROUP_ID))
async def leech_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    user = message.from_user
    user_name = user.first_name if user else "Unknown"
    user_id = user.id if user else 0

    if not await check_fsub(client, user_id):
        await message.reply_text(
            "⚠️ **Force Subscription Required!**\n\n"
            "You must join our update channels below to use leech downloads.",
            reply_markup=await not_joined_keyboard()
        )
        return

    if not is_verified(user_id):
        keyboard = await verification_keyboard(client, user_id)
        await message.reply_text(
            "⚠️ **Token Verification Required!**\n\n"
            "You haven't verified your token for the last 12 hours. Please complete the verification using the button below to start downloading.",
            reply_markup=keyboard
        )
        return

    url = ""
    raw_text = ""
    custom_name = None
    custom_thumb_source = None

    if message.reply_to_message:
        if message.reply_to_message.text:
            url = message.reply_to_message.text.strip()
        elif message.reply_to_message.caption:
            url = message.reply_to_message.caption.strip()
        elif message.reply_to_message.media:
            chat_id = message.reply_to_message.chat.id
            msg_id = message.reply_to_message.id
            if message.reply_to_message.chat.username:
                url = f"https://t.me/{message.reply_to_message.chat.username}/{msg_id}"
            else:
                chat_str = str(chat_id).replace("-100", "")
                url = f"https://t.me/c/{chat_str}/{msg_id}"

        if message.text and len(message.text.split(" ", 1)) > 1:
            raw_text = message.text.split(" ", 1)[1]

    if not url and message.text and len(message.text.split(" ", 1)) > 1:
        raw_text = message.text.split(" ", 1)[1]
        url = raw_text.split(" -n")[0].split(" -t")[0].strip()
    elif url and not raw_text and message.text and len(message.text.split(" ", 1)) > 1:
        raw_text = message.text.split(" ", 1)[1]

    if not url:
        await message.reply_text("❌ Please provide a link or reply to a message/media!\nExample: `/leech https://... -n video.mp4 -t thumbnail_url`")
        return

    if raw_text and "-t" in raw_text:
        parts = raw_text.split("-t")
        url = parts[0].split("-n")[0].strip() if "-n" in parts[0] else parts[0].strip()
        custom_thumb_source = parts[1].strip().split(" ")[0]
        if "-n" in raw_text:
            try:
                custom_name = raw_text.split("-n")[1].split("-t")[0].strip()
            except:
                pass
    elif raw_text and "-n" in raw_text:
        parts = raw_text.split("-n")
        url = parts[0].strip()
        custom_name = parts[1].strip().split(" -t")[0].strip()
        if "-t" in parts[1]:
            custom_thumb_source = parts[1].split("-t")[1].strip()

    if not is_premium(user_id):
        active_count = ACTIVE_TASKS.get(user_id, 0)
        if active_count >= USER_TASK_LIMIT:
            await message.reply_text(
                f"⚠️ **Limit Exceeded!**\n\n"
                f"You have `{active_count}` active downloads running. "
                f"Upgrade to Premium for unlimited downloads (Max allowed: {USER_TASK_LIMIT})."
            )
            return

    status_msg = await message.reply_text("⏳ Initializing download... Please wait.")
    
    if "t.me/" in url and "http" in url and len(url.split("t.me/")[1].split("/")) >= 2:
        await process_telegram_link(client, status_msg, user_id, user_name, url, custom_name, custom_thumb_source)
    else:
        await process_download(client, status_msg, user_id, user_name, url, custom_name, custom_thumb_source, 'best')

@app.on_message((filters.command("ytdl") | filters.command("yt")) & filters.chat(ALLOWED_GROUP_ID))
async def ytdl_handler(client: Client, message: Message):
    await send_random_reaction(client, message)
    user_id = message.from_user.id
    if not await check_fsub(client, user_id):
        await message.reply_text(
            "⚠️ **Force Subscription Required!**\n\n"
            "You must join our update channels below to use ytdl downloads.",
            reply_markup=await not_joined_keyboard()
        )
        return

    if not is_verified(user_id):
        keyboard = await verification_keyboard(client, user_id)
        await message.reply_text(
            "⚠️ **Token Verification Required!**\n\n"
            "You haven't verified your token for the last 12 hours. Please complete the verification using the button below to start downloading.",
            reply_markup=keyboard
        )
        return

    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a YouTube link!\nExample: `/ytdl https://youtu.be/xxxx`")
        return

    url = message.command[1]
    USER_YTDL_LINKS[user_id] = url

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 144p", callback_data="ytdl_144")],
        [InlineKeyboardButton("📥 240p", callback_data="ytdl_240")],
        [InlineKeyboardButton("📥 360p", callback_data="ytdl_360")],
        [InlineKeyboardButton("📥 480p", callback_data="ytdl_480")],
        [InlineKeyboardButton("📥 720p", callback_data="ytdl_720")],
        [InlineKeyboardButton("📥 1080p", callback_data="ytdl_1080")],
        [InlineKeyboardButton("🎵 MP3 Audio", callback_data="ytdl_mp3")]
    ])

    await message.reply_text(
        "👇 **Select video quality format:**",
        reply_markup=keyboard
    )

async def process_telegram_link(client, status_msg, user_id, user_name, url, custom_name, custom_thumb_source):
    ACTIVE_TASKS[user_id] = ACTIVE_TASKS.get(user_id, 0) + 1
    downloaded_file = None
    custom_thumb_path = None
    auto_thumb_path = None

    try:
        parts = url.strip("/").split("/")
        msg_id_str = parts[-1]
        if not msg_id_str.isdigit():
            raise Exception("Invalid Telegram link message ID!")
        msg_id = int(msg_id_str)
        
        channel_username = parts[-2]
        if "c" in parts:
            channel_username = int("-100" + parts[-2])

        await status_msg.edit_text("🔍 Fetching message from Telegram channel...")
        target_msg = await client.get_messages(channel_username, msg_id)

        if not target_msg or not target_msg.media:
            raise Exception("No media found in the given Telegram link or message is empty!")

        await status_msg.edit_text("📥 Downloading media from Telegram (Full File)...")
        
        # Fixed: Ensuring full file download using download_media properly without truncation
        downloaded_file = await client.download_media(
            target_msg,
            file_name="downloads/"
        )

        if not downloaded_file or not os.path.exists(downloaded_file):
            raise Exception("Failed to download media from Telegram link.")

        file_size = os.path.getsize(downloaded_file)
        ext = os.path.splitext(downloaded_file)[1]
        original_basename = os.path.basename(downloaded_file)

        if custom_name:
            file_title = custom_name if custom_name.endswith(ext) else custom_name + ext
            new_file_path = os.path.join("downloads", file_title)
            os.rename(downloaded_file, new_file_path)
            downloaded_file = new_file_path
        else:
            file_title = original_basename

        start_time = time.time()
        last_upload_update = 0

        def upload_progress(current, total):
            nonlocal last_upload_update
            if user_id in CANCEL_REQUESTS:
                return

            current_time = time.time()
            if current_time - last_upload_update > 3 or current == total:
                last_upload_update = current_time
                elapsed_time = current_time - start_time
                
                percentage = (current / total) * 100 if total > 0 else 0
                bar = get_progress_bar(percentage)
                
                speed = current / elapsed_time if elapsed_time > 0 else 0
                eta = (total - current) / speed if speed > 0 else 0
                
                upload_str = (
                    f"📤 **Uploading · {percentage:.1f}%**\n"
                    f"🎬 <code>{file_title}</code>\n\n"
                    f"{bar} {percentage:.1f}%\n"
                    f" ┣ 💾 **Size:** {human_bytes(current)} / {human_bytes(total)}\n"
                    f" ┣ ⚡ **Speed:** {human_bytes(speed)}/s\n"
                    f" ┗ ⏱️ **ETA:** {int(eta)}s"
                )
                try:
                    client.loop.create_task(
                        status_msg.edit_text(
                            upload_str,
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("✖️ Task Cancel", callback_data=f"cancel_dl_{user_id}")]
                            ])
                        )
                    )
                except Exception:
                    pass

        caption = (
            f"<b>{file_title}</b>\n\n"
            f"👤 <b>Task By:</b> {user_name} (`{user_id}`)\n"
            f"📦 <b>Size:</b> {human_bytes(file_size)}\n"
            f"🔗 <b>Link:</b> {url}"
        )

        valid_thumb = None
        if custom_thumb_source:
            custom_thumb_path = await download_thumbnail_from_source(client, custom_thumb_source, user_id)
            if custom_thumb_path and os.path.exists(custom_thumb_path):
                valid_thumb = custom_thumb_path

        if not valid_thumb:
            thumb = USER_THUMBNAILS.get(user_id)
            valid_thumb = thumb if thumb and os.path.exists(thumb) else None

        duration, width, height = 0, 0, 0
        if target_msg.video or target_msg.animation:
            video_obj = target_msg.video or target_msg.animation
            duration = video_obj.duration
            width = video_obj.width
            height = video_obj.height
            if not valid_thumb:
                auto_thumb_path = generate_thumbnail(downloaded_file, user_id)
                valid_thumb = auto_thumb_path

        file_mode = USER_FILE_MODES.get(user_id, "video")

        if file_mode == "document" or not (target_msg.video or target_msg.audio):
            sent_msg = await client.send_document(
                chat_id=status_msg.chat.id,
                document=downloaded_file,
                caption=caption,
                thumb=valid_thumb,
                progress=upload_progress,
                reply_to_message_id=status_msg.reply_to_message_id
            )
        elif target_msg.audio:
            sent_msg = await client.send_audio(
                chat_id=status_msg.chat.id,
                audio=downloaded_file,
                caption=caption,
                thumb=valid_thumb,
                progress=upload_progress,
                reply_to_message_id=status_msg.reply_to_message_id
            )
        else:
            sent_msg = await client.send_video(
                chat_id=status_msg.chat.id,
                video=downloaded_file,
                caption=caption,
                duration=duration,
                width=width,
                height=height,
                thumb=valid_thumb,
                progress=upload_progress,
                reply_to_message_id=status_msg.reply_to_message_id
            )

        try:
            if sent_msg:
                await sent_msg.copy(chat_id=DATABASE_CHANNEL_ID)
        except Exception as db_err:
            logging.error(f"Failed to forward to Database Channel: {db_err}")

        log_text = (
            f"📥 <b>Telegram Link Download Completed!</b>\n\n"
            f"👤 <b>User:</b> {user_name} (`{user_id}`)\n"
            f"🔗 <b>URL:</b> {url}\n"
            f"📁 <b>File:</b> {file_title}\n"
            f"📦 <b>Size:</b> {human_bytes(file_size)}"
        )
        try:
            await client.send_message(chat_id=LOG_CHANNEL_ID, text=log_text)
        except Exception as e:
            logging.error(f"Failed to send log to LOG_CHANNEL: {e}")

        if downloaded_file and os.path.exists(downloaded_file):
            os.remove(downloaded_file)
        if auto_thumb_path and os.path.exists(auto_thumb_path):
            os.remove(auto_thumb_path)
        if custom_thumb_path and os.path.exists(custom_thumb_path):
            os.remove(custom_thumb_path)

        await status_msg.delete()

    except Exception as e:
        error_msg = (
            f"⚠️ <b>Telegram Link Download Failed!</b>\n\n"
            f"<b>User:</b> {user_name} (`{user_id}`)\n"
            f"<b>URL:</b> `{url}`\n"
            f"<b>Error Details:</b> `{str(e)}`"
        )
        try:
            await client.send_message(chat_id=LOG_CHANNEL_ID, text=error_msg)
        except Exception:
            pass
        
        try:
            await status_msg.edit_text(f"❌ **Task Failed!**\n\n**Reason:** `{str(e)}`")
        except Exception:
            pass

        if downloaded_file and os.path.exists(downloaded_file):
            os.remove(downloaded_file)
        if auto_thumb_path and os.path.exists(auto_thumb_path):
            os.remove(auto_thumb_path)
        if custom_thumb_path and os.path.exists(custom_thumb_path):
            os.remove(custom_thumb_path)

    finally:
        if user_id in ACTIVE_TASKS:
            ACTIVE_TASKS[user_id] -= 1
            if ACTIVE_TASKS[user_id] <= 0:
                del ACTIVE_TASKS[user_id]

async def process_download(client, status_msg, user_id, user_name, url, custom_name, custom_thumb_source, quality):
    ACTIVE_TASKS[user_id] = ACTIVE_TASKS.get(user_id, 0) + 1
    
    file_path = None
    auto_thumb_path = None
    custom_thumb_path = None
    
    try:
        os.makedirs("downloads", exist_ok=True)
        last_update_time = 0

        cancel_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✖️ Task Cancel", callback_data=f"cancel_dl_{user_id}")]
        ])

        def download_progress(d):
            nonlocal last_update_time
            if user_id in CANCEL_REQUESTS:
                raise Exception("Task cancelled by user/admin.")

            if d['status'] == 'downloading':
                current_time = time.time()
                if current_time - last_update_time > 3:
                    last_update_time = current_time
                    filename = d.get('filename', 'Video')
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    
                    if total > 0:
                        percentage = (downloaded / total) * 100
                        progress_str = f"📥 **Downloading...**\n\n" \
                                       f"📁 **File:** `{os.path.basename(filename)}`\n" \
                                       f"📊 **Progress:** `{percentage:.1f}%`\n" \
                                       f"📦 **Size:** `{human_bytes(downloaded)} / {human_bytes(total)}`"
                    else:
                        progress_str = f"📥 **Downloading...**\n\n" \
                                       f"📁 **File:** `{os.path.basename(filename)}`\n" \
                                       f"📦 **Downloaded:** `{human_bytes(downloaded)}`"
                    
                    try:
                        client.loop.create_task(status_msg.edit_text(progress_str, reply_markup=cancel_keyboard))
                    except Exception:
                        pass

        common_ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'max_filesize': 2000 * 1024 * 1024,
            'progress_hooks': [download_progress],
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                }
            },
            'geo_bypass': True,
            'nocheckcertificate': True,
        }

        if quality == 'mp3':
            ydl_opts = {
                **common_ydl_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        elif quality == 'best':
            ydl_opts = {
                **common_ydl_opts,
                'format': 'best',
            }
        else:
            ydl_opts = {
                **common_ydl_opts,
                'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best',
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            if quality == 'mp3':
                file_path = os.path.splitext(file_path)[0] + ".mp3"
            
            original_title = info_dict.get('title', 'Media')
            ext = os.path.splitext(file_path)[1]
            
            if custom_name:
                file_title = custom_name if custom_name.endswith(ext) else custom_name + ext
                new_file_path = os.path.join("downloads", file_title)
                if os.path.exists(file_path):
                    os.rename(file_path, new_file_path)
                    file_path = new_file_path
            else:
                file_title = original_title + ext if not original_title.endswith(ext) else original_title

            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

        if user_id in CANCEL_REQUESTS:
            raise Exception("Task cancelled by user/admin.")

        start_time = time.time()
        last_upload_update = 0

        def upload_progress(current, total):
            nonlocal last_upload_update
            if user_id in CANCEL_REQUESTS:
                return

            current_time = time.time()
            if current_time - last_upload_update > 3 or current == total:
                last_upload_update = current_time
                elapsed_time = current_time - start_time
                
                percentage = (current / total) * 100 if total > 0 else 0
                bar = get_progress_bar(percentage)
                
                speed = current / elapsed_time if elapsed_time > 0 else 0
                eta = (total - current) / speed if speed > 0 else 0
                
                upload_str = (
                    f"📤 **Uploading · {percentage:.1f}%**\n"
                    f"🎬 <code>{file_title}</code>\n\n"
                    f"{bar} {percentage:.1f}%\n"
                    f" ┣ 💾 **Size:** {human_bytes(current)} / {human_bytes(total)}\n"
                    f" ┣ ⚡ **Speed:** {human_bytes(speed)}/s\n"
                    f" ┗ ⏱️ **ETA:** {int(eta)}s"
                )
                try:
                    client.loop.create_task(
                        status_msg.edit_text(
                            upload_str,
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("✖️ Task Cancel", callback_data=f"cancel_dl_{user_id}")]
                            ])
                        )
                    )
                except Exception:
                    pass

        caption = (
            f"<b>{file_title}</b>\n\n"
            f"👤 <b>Task By:</b> {user_name} (`{user_id}`)\n"
            f"📦 <b>Size:</b> {human_bytes(file_size)}\n"
            f"🔗 <b>Link:</b> {url}"
        )

        valid_thumb = None
        if custom_thumb_source:
            custom_thumb_path = await download_thumbnail_from_source(client, custom_thumb_source, user_id)
            if custom_thumb_path and os.path.exists(custom_thumb_path):
                valid_thumb = custom_thumb_path

        if not valid_thumb:
            thumb = USER_THUMBNAILS.get(user_id)
            valid_thumb = thumb if thumb and os.path.exists(thumb) else None

        if not valid_thumb and quality != 'mp3' and file_path:
            auto_thumb_path = generate_thumbnail(file_path, user_id)
            valid_thumb = auto_thumb_path

        duration, width, height = 0, 0, 0
        if quality != 'mp3' and file_path and os.path.exists(file_path):
            duration, width, height = get_video_info(file_path)

        file_mode = USER_FILE_MODES.get(user_id, "video")

        if quality == 'mp3' or file_mode == "document":
            sent_msg = await client.send_document(
                chat_id=status_msg.chat.id,
                document=file_path,
                caption=caption,
                thumb=valid_thumb,
                progress=upload_progress,
                reply_to_message_id=status_msg.reply_to_message_id
            )
        else:
            sent_msg = await client.send_video(
                chat_id=status_msg.chat.id,
                video=file_path,
                caption=caption,
                duration=duration,
                width=width,
                height=height,
                thumb=valid_thumb,
                progress=upload_progress,
                reply_to_message_id=status_msg.reply_to_message_id
            )

        try:
            if sent_msg:
                await sent_msg.copy(chat_id=DATABASE_CHANNEL_ID)
        except Exception as db_err:
            logging.error(f"Failed to forward to Database Channel: {db_err}")

        log_text = (
            f"📥 <b>New Download Completed!</b>\n\n"
            f"👤 <b>User:</b> {user_name} (`{user_id}`)\n"
            f"🔗 <b>URL:</b> {url}\n"
            f"📁 <b>File:</b> {file_title}\n"
            f"📦 <b>Size:</b> {human_bytes(file_size)}"
        )
        try:
            await client.send_message(chat_id=LOG_CHANNEL_ID, text=log_text)
        except Exception as e:
            logging.error(f"Failed to send log to LOG_CHANNEL: {e}")

        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        if auto_thumb_path and os.path.exists(auto_thumb_path):
            os.remove(auto_thumb_path)
        if custom_thumb_path and os.path.exists(custom_thumb_path):
            os.remove(custom_thumb_path)
            
        await status_msg.delete()

    except Exception as e:
        error_msg = (
            f"⚠️ <b>Download Failed / Error Occurred!</b>\n\n"
            f"<b>User:</b> {user_name} (`{user_id}`)\n"
            f"<b>URL:</b> `{url}`\n"
            f"<b>Error Details:</b> `{str(e)}`"
        )
        try:
            await client.send_message(chat_id=LOG_CHANNEL_ID, text=error_msg)
        except Exception:
            pass
        
        try:
            await status_msg.edit_text(f"❌ **Task Cancelled / Failed!**\n\n**Reason:** `{str(e)}`")
        except Exception:
            pass

        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        if auto_thumb_path and os.path.exists(auto_thumb_path):
            os.remove(auto_thumb_path)
        if custom_thumb_path and os.path.exists(custom_thumb_path):
            os.remove(custom_thumb_path)
            
    finally:
        if user_id in CANCEL_REQUESTS:
            CANCEL_REQUESTS.remove(user_id)
        if user_id in ACTIVE_TASKS:
            ACTIVE_TASKS[user_id] -= 1
            if ACTIVE_TASKS[user_id] <= 0:
                del ACTIVE_TASKS[user_id]

# ----------------- Group-Only File Renaming & Downloading Handlers -----------------

@app.on_message((filters.document | filters.video) & filters.chat(ALLOWED_GROUP_ID))
async def send_rename_button(client, message):
    if not await check_fsub(client, message.from_user.id):
        return
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ File Renaming", callback_data="start_rename")]
    ])
    await message.reply_text("Click the button below if you want to rename this file:", reply_markup=keyboard)

@app.on_message(filters.text & filters.chat(ALLOWED_GROUP_ID) & ~filters.command("/"))
async def handle_new_name(client, message: Message):
    user_id = message.from_user.id
    
    if USER_STATES.get(user_id) == "waiting_for_name":
        new_name = message.text.strip()
        USER_STATES[user_id] = None
        
        try:
            await message.delete()
        except Exception as e:
            logging.error(f"Error deleting message: {e}")
            
        data_info = RENAME_DATA.get(user_id)
        if not data_info:
            await message.reply_text("❌ Session expired. Please try again.")
            return

        # Store new_name in RENAME_DATA temporarily and ask for format (Video / Document)
        RENAME_DATA[user_id]["new_name"] = new_name
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📹 Video Format", callback_data="rename_mode_video"),
                InlineKeyboardButton("📁 Document Format", callback_data="rename_mode_document")
            ]
        ])
        
        await message.reply_text(
            f"✨ **New Name set to:** `{new_name}`\n\n"
            f"👇 **Choose upload format:**",
            reply_markup=keyboard
        )

async def process_renamed_file(client, status_msg, user_id, user_name, original_msg, new_name, mode):
    if not original_msg or not original_msg.media:
        await status_msg.edit_text("❌ Original media message not found or invalid!")
        return

    downloaded_file = None
    auto_thumb_path = None
    try:
        os.makedirs("downloads", exist_ok=True)
        await status_msg.edit_text("📥 Downloading file for renaming (Full File)...")
        
        # Fixed: Ensuring full file download without truncation
        downloaded_file = await client.download_media(
            original_msg,
            file_name="downloads/"
        )

        if not downloaded_file or not os.path.exists(downloaded_file):
            raise Exception("Failed to download file.")

        ext = os.path.splitext(new_name)[1]
        if not ext:
            old_ext = os.path.splitext(downloaded_file)[1]
            file_title = new_name + old_ext
        else:
            file_title = new_name

        new_file_path = os.path.join("downloads", file_title)
        if downloaded_file != new_file_path:
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            os.rename(downloaded_file, new_file_path)
            downloaded_file = new_file_path
            
        file_size = os.path.getsize(downloaded_file)

        start_time = time.time()
        last_upload_update = 0

        def upload_progress(current, total):
            nonlocal last_upload_update
            current_time = time.time()
            if current_time - last_upload_update > 3 or current == total:
                last_upload_update = current_time
                elapsed_time = current_time - start_time
                percentage = (current / total) * 100 if total > 0 else 0
                bar = get_progress_bar(percentage)
                speed = current / elapsed_time if elapsed_time > 0 else 0
                eta = (total - current) / speed if speed > 0 else 0
                
                upload_str = (
                    f"📤 **Uploading Renamed File · {percentage:.1f}%**\n"
                    f"🎬 <code>{file_title}</code>\n\n"
                    f"{bar} {percentage:.1f}%\n"
                    f" ┣ 💾 **Size:** {human_bytes(current)} / {human_bytes(total)}\n"
                    f" ┣ ⚡ **Speed:** {human_bytes(speed)}/s\n"
                    f" ┗ ⏱️ **ETA:** {int(eta)}s"
                )
                try:
                    client.loop.create_task(status_msg.edit_text(upload_str))
                except Exception:
                    pass

        caption = (
            f"<b>{file_title}</b>\n\n"
            f"👤 <b>Task By:</b> {user_name} (`{user_id}`)\n"
            f"📦 <b>Size:</b> {human_bytes(file_size)}"
        )

        thumb = USER_THUMBNAILS.get(user_id)
        valid_thumb = thumb if thumb and os.path.exists(thumb) else None

        duration, width, height = 0, 0, 0
        file_ext = os.path.splitext(file_title)[1].lower()

        if file_ext in [".mp4", ".mkv", ".avi", ".mov", ".webm"]:
            duration, width, height = get_video_info(downloaded_file)
            if not valid_thumb:
                auto_thumb_path = generate_thumbnail(downloaded_file, user_id)
                valid_thumb = auto_thumb_path

        if mode == "document" or file_ext == ".mp3":
            sent_msg = await client.send_document(
                chat_id=status_msg.chat.id,
                document=downloaded_file,
                caption=caption,
                thumb=valid_thumb,
                progress=upload_progress
            )
        else:
            sent_msg = await client.send_video(
                chat_id=status_msg.chat.id,
                video=downloaded_file,
                caption=caption,
                duration=duration,
                width=width,
                height=height,
                thumb=valid_thumb,
                progress=upload_progress
            )

        try:
            if sent_msg:
                await sent_msg.copy(chat_id=DATABASE_CHANNEL_ID)
        except Exception as db_err:
            logging.error(f"Failed to forward to Database Channel: {db_err}")

        if downloaded_file and os.path.exists(downloaded_file):
            os.remove(downloaded_file)
        if auto_thumb_path and os.path.exists(auto_thumb_path):
            os.remove(auto_thumb_path)

        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ **Rename & Upload Failed!**\n\n**Reason:** `{str(e)}`")
        if downloaded_file and os.path.exists(downloaded_file):
            os.remove(downloaded_file)
        if auto_thumb_path and os.path.exists(auto_thumb_path):
            os.remove(auto_thumb_path)

# ---------------------------------------------------------------------------------------------------------------

async def main():
    await start_web_server()
    await app.start()
    print("🤖 Leech Bot Started Successfully...")
    await idle()

if __name__ == "__main__":
    app.run(main())
