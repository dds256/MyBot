import base64
import httpx
import os
from pyrogram import filters, Client
from config import BOT_USERNAME
from AKDBOT import app
from uuid import uuid4
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.reply & filters.command("upscale"))
async def upscale_image(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply_text("Please reply to an image to upscale it.")
            return

        image = message.reply_to_message.photo.file_id
        file_path = await client.download_media(image)

        with open(file_path, "rb") as image_file:
            f = image_file.read()

        b = base64.b64encode(f).decode("utf-8")

        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                "https://api.qewertyy.me/upscale", json={"image_data": b}, timeout=None
            )

        if response.status_code != 200:
            await message.reply_text("Failed to upscale the image. Please try again later.")
            return

        upscaled_image_path = "upscaled.png"
        with open(upscaled_image_path, "wb") as output_file:
            output_file.write(response.content)

        await client.send_document(
            message.chat.id,
            document=upscaled_image_path,
            caption="Here is the upscaled image!"
        )

        os.remove(file_path)
        os.remove(upscaled_image_path)

    except Exception as e:
        print(f"Failed to upscale the image: {e}")
        await message.reply_text("Failed to upscale the image. Please try again later.")

# ------------

import requests

waifu_api_url = 'https://api.waifu.im/search'

def get_waifu_data(tags):
    params = {
        'included_tags': tags,
        'height': '>=2000'
    }

    response = requests.get(waifu_api_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.on_message(filters.command("waifu"))
def waifu_command(client, message):
    try:
        tags = ['maid']  # You can customize the tags as needed
        waifu_data = get_waifu_data(tags)

        if waifu_data and 'images' in waifu_data:
            first_image = waifu_data['images'][0]
            image_url = first_image['url']
            message.reply_photo(image_url)
        else:
            message.reply_text("No waifu found with the specified tags.")

    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")
        