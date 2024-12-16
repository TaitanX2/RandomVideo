from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import random

# Replace with your API credentials and bot token
API_ID = "12380656"
API_HASH = "d927c13beaaf5110f25c505b7c071273"
BOT_TOKEN = "8009994082:AAGf7QrGIfQJ7gIZVEJT6_RgVwu-kbTzZ10"
CHANNEL_ID = -1002279954639  # Replace with your channel's numeric ID (start with -100)

# MongoDB connection
MONGO_URI = "mongodb+srv://rr:rr@cluster0.5pjchfv.mongodb.net/?retryWrites=true&w=majority"  # Replace with your MongoDB connection string
client = MongoClient(MONGO_URI)
db = client["random_video_bot"]  # Database name
videos_collection = db["videos"]  # Collection name

# Initialize the bot
bot = Client("random_video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Fetch all video messages from the channel and save to MongoDB
async def fetch_and_cache_videos(client):
    videos = []
    async for message in client.search_messages(CHANNEL_ID, filter="video"):
        if message.video:
            videos.append({"file_id": message.video.file_id})
    if videos:
        videos_collection.delete_many({})  # Clear the old cache
        videos_collection.insert_many(videos)  # Insert new videos into the database
    return videos

# Retrieve cached videos from MongoDB
def get_cached_videos():
    return list(videos_collection.find())

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
    videos = get_cached_videos()
    if not videos:  # If no videos are cached, fetch from the channel
        await fetch_and_cache_videos(client)
        videos = get_cached_videos()

    if videos:
        random_video = random.choice(videos)
        await client.send_video(
            chat_id=callback_query.message.chat.id,
            video=random_video["file_id"],
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
