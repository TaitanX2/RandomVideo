import random
from pyrogram.types import InputMediaVideo, InlineKeyboardMarkup, InlineKeyboardButton

# Channel ID (replace with your channel username or ID)
CHANNEL_ID = "@your_channel_username"  # Example: "123456789" or "@mychannel"

# Fetch Random Video from Channel
async def fetch_random_video(channel_id):
    try:
        # Fetching messages from the channel
        messages = []
        async for message in bot.get_chat_history(channel_id, limit=100):
            if message.video:
                messages.append(message)

        if not messages:
            LOGGER.info("No videos found in the channel.")
            return None

        # Select a random video
        random_video = random.choice(messages)
        return random_video
    except Exception as e:
        LOGGER.error(f"Error fetching random video: {e}")
        return None

# Command to send random video with inline button
@bot.on_message(cdx("randomvideo") & ~pyrofl.bot)
async def send_random_video(client, message):
    try:
        # Fetch a random video
        random_video = await fetch_random_video(CHANNEL_ID)
        if not random_video:
            await message.reply_text("No videos found in the channel.")
            return

        # Inline buttons
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📢 Visit Channel", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"
                    ),
                    InlineKeyboardButton(
                        text="🔄 Get Another", callback_data="get_new_video"
                    ),
                ]
            ]
        )

        # Sending the random video with buttons
        await message.reply_video(
            video=random_video.video.file_id,
            caption="🎥 Here's a random video from the channel!",
            reply_markup=buttons,
        )
    except Exception as e:
        LOGGER.error(f"Error sending random video: {e}")
        await message.reply_text("Failed to fetch a random video.")

# Callback for fetching another random video
@bot.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "get_new_video":
        try:
            # Fetch another random video
            random_video = await fetch_random_video(CHANNEL_ID)
            if not random_video:
                await callback_query.answer("No more videos found in the channel.")
                return

            # Editing the message to replace with a new random video
            await callback_query.message.edit_media(
                media=InputMediaVideo(
                    media=random_video.video.file_id,
                    caption="🎥 Here's another random video from the channel!"
                ),
                reply_markup=callback_query.message.reply_markup,
            )
        except Exception as e:
            LOGGER.error(f"Error fetching another video: {e}")
            await callback_query.answer("Failed to fetch a new video.")