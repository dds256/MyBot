import aiohttp
import random
import string
from aiohttp import ContentTypeError
from pyrogram import filters
from AKDBOT import app as app
import json

# PasteBin API details
PASTEBIN_API_KEY = 'e-zy2euWaViTYmi61-KVxPh_KVVvacUP'
PASTEBIN_API_URL = 'https://pastebin.com/api/api_post.php'

async def upload_to_pastebin(content, title=None, visibility=None, expiration=None, format=None):
    data = {
        'api_dev_key': PASTEBIN_API_KEY,
        'api_option': 'paste',
        'api_paste_code': content
    }
    if title:
        data['api_paste_name'] = title
    if visibility:
        data['api_paste_private'] = visibility
    if expiration:
        data['api_paste_expire_date'] = expiration
    if format:
        data['api_paste_format'] = format

    async with aiohttp.ClientSession() as session:
        async with session.post(PASTEBIN_API_URL, data=data) as response:
            if response.status != 200:
                return False, f"HTTP Error: {response.status}"
            return True, await response.text()

async def handle_upload_command(bot, message):
    args = message.command[1:]

    content = None
    title = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Generate a random title

    # Check if the command has arguments
    if not args:
        # Check if there's a reply
        replied = message.reply_to_message
        if replied and replied.text:
            content = replied.text
        else:
            return await message.reply("Please provide text to post, for example /pastebin your paste | or by replying to a message with text.")
    else:
        content = ' '.join(args)

    # Check if the content is a valid JSON
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            title = data.get("title", title)
            description = data.get("description", "")
            download_link = data.get("download", "")
            content = f"Title: {title}\nDescription: {description}\nDownload: {download_link}"
    except json.JSONDecodeError:
        # If not JSON, proceed with the content as is
        pass

    if not content:
        return await message.reply("No content provided to post. example: /pastebin this is a paste")

    upload_msg = await message.reply("Processing...")

    success, result = await upload_to_pastebin(content, title)
    if not success:
        return await upload_msg.edit(f"Upload failed: {result}")

    # Add '/raw/' to the URL for the raw link
    paste_key = result.split('/')[-1]
    raw_link = f"https://pastebin.com/raw/{paste_key}"

    await message.reply_text(f"Here's your raw link: {raw_link}\nCopyable Link: `{raw_link}`", disable_web_page_preview=True)
    await upload_msg.delete()

@app.on_message(filters.command("pastebin"))
async def upload_pastebin(bot, message):
    await handle_upload_command(bot, message)
    