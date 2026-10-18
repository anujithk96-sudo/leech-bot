import os
import yt_dlp
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import app

# Path for YouTube Cookies file
COOKIE_FILE = "cookies.txt"

# Handler for /yt and /ytdl commands only
@app.on_message(filters.command(["yt", "ytdl"]))
async def youtube_download_handler(client, message):
    # Check if the link is provided with the command
    if len(message.command) < 2:
        await message.reply_text("Please provide a YouTube link!\nExample: `/yt <link>` or `/ytdl <link>`")
        return

    url = message.command[1]
    
    if not url.startswith("http"):
        await message.reply_text("Invalid YouTube link!")
        return

    # Inline buttons stacked vertically (one by one) in English
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 144p", callback_data=f"dl|144|{url}")],
        [InlineKeyboardButton("🎬 240p", callback_data=f"dl|240|{url}")],
        [InlineKeyboardButton("🎬 360p", callback_data=f"dl|360|{url}")],
        [InlineKeyboardButton("🎬 480p", callback_data=f"dl|480|{url}")],
        [InlineKeyboardButton("🎬 720p", callback_data=f"dl|720|{url}")],
        [InlineKeyboardButton("🎬 1080p", callback_data=f"dl|1080|{url}")],
        [InlineKeyboardButton("🎵 MP3 Audio", callback_data=f"dl|mp3|{url}")]
    ])

    await message.reply_text(
        "YouTube link received! Please select your preferred quality below:",
        reply_markup=keyboard
    )

# Callback query handler for downloads
@app.on_callback_query(filters.regex("^dl\\|"))
async def button_download_callback(client, callback_query):
    data = callback_query.data.split("|")
    quality = data[1]
    url = data[2]

    await callback_query.message.edit_text("⏳ Downloading, please wait...")

    try:
        ydl_opts = {
            'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
            'outtmpl': '%(title)s.%(ext)s',
        }

        if quality == "mp3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if quality == "mp3":
                filename = filename.rsplit(".", 1)[0] + ".mp3"

        # Sending file to Telegram
        await callback_query.message.reply_document(
            document=filename,
            caption="Here is your file! 🎉"
        )
        
        # Cleaning up local storage
        if os.path.exists(filename):
            os.remove(filename)
            
        await callback_query.message.delete()

    except Exception as e:
        await callback_query.message.edit_text(f"❌ Download failed!\n\n**Reason:** `{str(e)}`")
