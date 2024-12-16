from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# Replace with your API credentials and bot token
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
CHANNEL_ID = -1001234567890  # Replace with your channel's numeric ID (start with -100)

# Initialize the bot
bot = Client("random_video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Fetch all video messages from the channel
async def fetch_videos(client):
    videos = []
    async for message in client.search_messages(CHANNEL_ID, filter="video"):
        if message.video:
            videos.append(message)
    return videos

# Handle /start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hello! Press the 'Generate' button to get a random video.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Generate", callback_data="generate")]]
        ),
    )

# Handle button callback
@bot.on_callback_query(filters.regex("generate"))
async def send_random_video(client, callback_query):
    videos = await fetch_videos(client)
    if videos:
        random_video = random.choice(videos)
        await client.send_video(
            chat_id=callback_query.message.chat.id,
            video=random_video.video.file_id,
            caption="Here's a random video!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Generate", callback_data="generate")]]
            ),
        )
        await callback_query.answer()
    else:
        await callback_query.answer("No videos found in the channel!", show_alert=True)

# Run the bot
if __name__ == "__main__":
    bot.run()
