import os
import asyncio
import logging
import tempfile
import shutil
from urllib.parse import urlparse

import yt_dlp
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import app

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cookies file
COOKIE_FILE = "cookies.txt"

# Temporary storage for YouTube links
youtube_jobs = {}


def is_valid_youtube_url(url):
    """Check whether the URL belongs to YouTube."""
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()

        return (
            parsed.scheme in ("http", "https")
            and (
                host == "youtube.com"
                or host.endswith(".youtube.com")
                or host == "youtu.be"
            )
        )
    except Exception:
        return False


def download_youtube(url, quality):
    """Download a YouTube video or audio."""

    temp_dir = tempfile.mkdtemp(prefix="yt_download_")

    try:
        ydl_opts = {
            "outtmpl": os.path.join(
                temp_dir,
                "%(title).100s [%(id)s].%(ext)s"
            ),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "retries": 3,
            "fragment_retries": 3,
            "socket_timeout": 30,
            "overwrites": True,
        }

        # Use cookies when the file exists.
        if os.path.isfile(COOKIE_FILE):
            ydl_opts["cookiefile"] = COOKIE_FILE

        if quality == "mp3":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            })

        else:
            height = int(quality)

            ydl_opts.update({
                "format": (
                    f"bestvideo[height<={height}]+bestaudio/"
                    f"best[height<={height}]/best"
                ),
                "merge_output_format": "mp4",
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # FFmpeg may change the final extension.
        if quality == "mp3":
            filename = os.path.splitext(filename)[0] + ".mp3"

        elif not os.path.isfile(filename):
            mp4_candidate = os.path.splitext(filename)[0] + ".mp4"

            if os.path.isfile(mp4_candidate):
                filename = mp4_candidate

        # Find the actual output if the extension differs.
        if not os.path.isfile(filename):
            files = [
                os.path.join(temp_dir, name)
                for name in os.listdir(temp_dir)
                if os.path.isfile(os.path.join(temp_dir, name))
                and not name.endswith((".part", ".ytdl"))
            ]

            if not files:
                raise FileNotFoundError(
                    "Downloaded file was not found."
                )

            filename = max(files, key=os.path.getsize)

        return filename, temp_dir

    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


@app.on_message(filters.command(["yt", "ytdl"]))
async def youtube_download_handler(client, message):

    if len(message.command) < 2:
        await message.reply_text(
            "❌ Please provide a YouTube link.\n\n"
            "Example:\n"
            "/yt https://youtu.be/VIDEO_ID"
        )
        return

    url = message.command[1].strip()

    if not is_valid_youtube_url(url):
        await message.reply_text(
            "❌ Invalid YouTube URL!\n"
            "Please send a valid YouTube video link."
        )
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 144p", callback_data="ytq:144")],
        [InlineKeyboardButton("🎬 240p", callback_data="ytq:240")],
        [InlineKeyboardButton("🎬 360p", callback_data="ytq:360")],
        [InlineKeyboardButton("🎬 480p", callback_data="ytq:480")],
        [InlineKeyboardButton("🎬 720p", callback_data="ytq:720")],
        [InlineKeyboardButton("🎬 1080p", callback_data="ytq:1080")],
        [InlineKeyboardButton("🎵 MP3 Audio", callback_data="ytq:mp3")],
    ])

    sent = await message.reply_text(
        "✅ YouTube link received!\n\n"
        "Select your preferred quality:",
        reply_markup=keyboard,
    )

    # Store the URL against this message.
    youtube_jobs[(sent.chat.id, sent.id)] = url


@app.on_callback_query(
    filters.regex(r"^ytq:(144|240|360|480|720|1080|mp3)$")
)
async def youtube_quality_callback(client, callback_query):

    key = (
        callback_query.message.chat.id,
        callback_query.message.id,
    )

    url = youtube_jobs.get(key)

    if not url:
        await callback_query.answer(
            "Link expired. Please send the YouTube URL again.",
            show_alert=True,
        )
        return

    quality = callback_query.data.split(":", 1)[1]

    await callback_query.answer()

    status = await callback_query.message.edit_text(
        f"⏳ Downloading {'MP3 audio' if quality == 'mp3' else quality + 'p video'}..."
    )

    filename = None
    temp_dir = None

    try:
        filename, temp_dir = await asyncio.to_thread(
            download_youtube,
            url,
            quality,
        )

        if not os.path.isfile(filename):
            raise FileNotFoundError(
                "Downloaded file does not exist."
            )

        await status.edit_text("📤 Uploading file to Telegram...")

        caption = (
            "🎵 YouTube MP3 Audio"
            if quality == "mp3"
            else f"🎬 YouTube Video — {quality}p"
        )

        await client.send_document(
            chat_id=callback_query.message.chat.id,
            document=filename,
            caption=caption,
            reply_to_message_id=callback_query.message.id,
        )

        await status.delete()
        youtube_jobs.pop(key, None)

    except Exception as e:
        logger.exception("YouTube download failed")

        error_text = str(e).replace("`", "'")

        if len(error_text) > 2000:
            error_text = error_text[:2000]

        try:
            await status.edit_text(
                "❌ Download failed!\n\n"
                f"**Reason:** `{error_text}`"
            )
        except Exception:
            pass

    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
