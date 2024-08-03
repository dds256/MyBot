import os
import aiohttp
import aiofiles
from aiohttp import ContentTypeError
from AKDBOT import app as app
from pyrogram import filters

# ImageBB API details
IMAGEBB_API_KEY = '900c4bbc479ea8441fab7f142c4632ce'
IMAGEBB_API_URL = 'https://api.imgbb.com/1/upload'

def check_filename(filroid):
    if os.path.exists(filroid):
        no = 1
        while True:
            ult = "{0}_{2}{1}".format(*os.path.splitext(filroid) + (no,))
            if os.path.exists(ult):
                no += 1
            else:
                return ult
    return filroid

async def upload_to_imagebb(file_path):
    url = f"{IMAGEBB_API_URL}?key={IMAGEBB_API_KEY}"
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            form_data = aiohttp.FormData()
            form_data.add_field('image', f)
            async with session.post(url, data=form_data) as response:
                if response.status != 200:
                    return False, f"HTTP Error: {response.status}"
                try:
                    result = await response.json()
                    if result['status'] != 200:
                        return False, result['error']['message']
                    return True, result['data']['url']
                except ContentTypeError:
                    return False, "Response content is not JSON"

@app.on_message(filters.command("upload"))
async def upload(bot, message):
    upload_msg = await message.reply("Processing...")
    replied = message.reply_to_message
    if not replied:
        return await upload_msg.edit("Reply to a photo to upload it to ImageBB")

    if replied.photo:
        photo = await bot.download_media(replied)
        name = check_filename(photo)
        os.rename(photo, name)
        success, result = await upload_to_imagebb(name)
        os.remove(name)
        if not success:
            return await upload_msg.edit(f"Upload failed: {result}")
        await message.reply_text(f"Here is your direct link: {result}")
        await upload_msg.delete()
        return
    await upload_msg.edit("Reply only to a photo to upload it to ImageBB")