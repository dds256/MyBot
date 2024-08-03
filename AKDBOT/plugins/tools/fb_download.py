import requests
from pyrogram import filters
from AKDBOT import app

# Function to download Facebook video using saveas.co API
async def download_facebook_video(link):
    try:
        api_url = "https://saveas.co/api/facebook"
        response = requests.post(api_url, data={"url": link})
        
        if response.ok:
            data = response.json()
            if data['success']:
                video_url = data['url']
                return video_url
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Improved regex to match various Facebook video URLs
FACEBOOK_VIDEO_REGEX = r'(https?:\/\/(?:www\.)?facebook\.com\/(?:reel|watch|video|videos|story\.php\?story_fbid=|[^\/]+\/videos\/)[^\s]+)'

@app.on_message(filters.command("fbdownload") | filters.regex(FACEBOOK_VIDEO_REGEX))
async def fbdownload_command(bot, message):
    try:
        link = None
        
        # Check if the message is a reply and contains a link
        if message.reply_to_message and message.reply_to_message.text:
            link = message.reply_to_message.text.strip()
            # Delete only the command message
            await message.delete()
            processing_message = await message.reply("Processing your Facebook video link...")
        else:
            # If not a reply, try to extract the link from the command message
            link = message.text.split(" ")[1]
            # Delete the command message
            await message.delete()
            # Send a progress message
            processing_message = await message.reply("Processing your Facebook video link...")
        
        # Download the Facebook video
        video_url = await download_facebook_video(link)
        
        if not video_url:
            await processing_message.edit("Failed to download Facebook video. Please ensure the link is valid.")
            return
        
        # Mention the user who requested the video in the caption
        caption = f"{message.from_user.mention}, here's your Facebook video."
        
        # Send the video with the caption
        await bot.send_video(message.chat.id, video_url, caption=caption)
        
        # Delete the progress message after sending the video
        await processing_message.delete()
    except IndexError:
        await message.reply("Please provide a valid Facebook video link.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
        