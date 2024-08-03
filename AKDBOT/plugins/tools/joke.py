import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from AKDBOT import app as app

# Function to get a random joke
async def get_joke():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://v2.jokeapi.dev/joke/Any") as response:
            if response.status == 200:
                return await response.json()
            return None

# Dictionary to store joke message IDs and corresponding user IDs
joke_message_ids = {}

# Enhanced sentiment analysis based on keywords and emojis
def analyze_sentiment(text):
    positive_keywords = [
        "haha", "lol", "funny", "hilarious", "good", "great", "awesome", "love" "nice",
        "😂", "🤣", "😊", "😁", "👍", "😆", "😹", "😄"
    ]
    negative_keywords = [
        "bad", "terrible", "boring", "not funny", "hate", "😠", "😡", "👎", "😒",
        "😞", "😤", "😢", "😭", "😩"
    ]

    text_lower = text.lower()

    if any(keyword in text_lower for keyword in positive_keywords):
        return "positive"
    elif any(keyword in text_lower for keyword in negative_keywords):
        return "negative"
    else:
        return "neutral"

@app.on_message(filters.command("joke"))
async def joke_command(bot, message):
    user = message.from_user
    processing_message = await message.reply("Fetching a joke...")
    
    try:
        joke_data = await get_joke()
        if not joke_data:
            await processing_message.edit("Failed to get a joke. Please try again later.")
            return
        
        joke = joke_data.get("joke") if "joke" in joke_data else f"{joke_data.get('setup')} - {joke_data.get('delivery')}"
        joke_monospace = f"`{joke}`"
        
        joke_message = await processing_message.edit(f"{user.mention}, here's your joke:\n{joke_monospace}")
        await message.delete()
        
        # Store the joke message ID and user ID
        joke_message_ids[joke_message.id] = user.id
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")

@app.on_message(filters.reply)
async def handle_reply(bot, message: Message):
    reply_to_message_id = message.reply_to_message.id
    
    if reply_to_message_id in joke_message_ids:
        user_id = joke_message_ids[reply_to_message_id]
        user = await bot.get_users(user_id)
        sentiment = analyze_sentiment(message.text)
        
        if sentiment == "positive":
            response = f"Glad you liked it, {user.mention}!"
        elif sentiment == "negative":
            response = f"Sorry to hear that, {user.mention}. I'll try to find a better joke next time!"
        else:
            response = f"Thanks for the feedback, {user.mention}!"

        await message.reply(response)