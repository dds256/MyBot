import base64
from pyrogram import filters
from pyrogram.types import Message
from AKDBOT import app
from AKDBOT.utils.errors import capture_err

def text_to_base64(text):
    base64_bytes = base64.b64encode(text.encode('utf-8'))
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def base64_to_text(base64_string):
    base64_bytes = base64_string.encode('utf-8')
    text_bytes = base64.b64decode(base64_bytes)
    text = text_bytes.decode('utf-8')
    return text

@app.on_message(filters.command("to_base64"))
@capture_err
async def to_base64_command(_, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text.strip()
    else:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.reply("Please provide text to convert to Base64.")
        text = args[1].strip()
    
    base64_string = text_to_base64(text)
    formatted_result = f"```\n{base64_string}\n```"
    await message.reply(formatted_result, parse_mode="Markdown")

@app.on_message(filters.command("from_base64"))
@capture_err
async def from_base64_command(_, message: Message):
    if message.reply_to_message:
        base64_string = message.reply_to_message.text.strip()
    else:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.reply("Please provide a Base64 string to convert to text.")
        base64_string = args[1].strip()
    
    try:
        text = base64_to_text(base64_string)
        formatted_result = f"```\n{text}\n```"
        await message.reply(formatted_result, parse_mode="Markdown")
    except (base64.binascii.Error, UnicodeDecodeError):
        await message.reply("Invalid Base64 string. Please provide a valid Base64 encoded string.")