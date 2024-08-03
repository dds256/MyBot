import requests
from pyrogram import filters
from AKDBOT import app
from bs4 import BeautifulSoup

# Function to download Instagram video using SaveIG
async def download_instagram_video(link):
    response = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
    if response.ok:
        data = response.json()
        html_content = data.get("data")
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            download_link = soup.find('a', {'title': 'Download Video'})
            if download_link:
                return download_link['href']
    return None

@app.on_message(filters.command("instadownload") | filters.regex(r'^https?:\/\/(?:www\.)?instagram\.com\/p\/[\w\-]+\/?$'))
async def instadownload_command(bot, message):
    try:
        link = None
        
        # Check if the message is a reply and contains a link
        if message.reply_to_message and message.reply_to_message.text:
            link = message.reply_to_message.text.strip()
            # Delete only the command message
            await message.delete()
            processing_message = await message.reply("Processing your Instagram link...")
        else:
            # If not a reply, try to extract the link from the command message
            link = message.text.split(" ")[1]
            # Delete the command message
            await message.delete()
            # Send a progress message
            processing_message = await message.reply("Processing your Instagram link...")
        
        # Download the Instagram video
        video_url = await download_instagram_video(link)
        
        if not video_url:
            await processing_message.edit("Failed to download Instagram video. Please ensure the link is valid.")
            return
        
        # Mention the user who requested the video in the caption
        caption = f"{message.from_user.mention}, Here's your Instagram video.."
        
        # Send the video with the caption
        await bot.send_video(message.chat.id, video_url, caption=caption)
        
        # Delete the progress message after sending the video
        await processing_message.delete()
    except IndexError:
        await message.reply("Please provide a valid Instagram video link.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
        