import base64
import os
import time
from pyrogram import filters
from pyrogram.types import Message
from PIL import Image
from AKDBOT import app
from AKDBOT.utils.errors import capture_err

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_bytes = base64.b64encode(image_file.read())
        base64_string = base64_bytes.decode('utf-8')
    return base64_string

def compress_image(input_image_path, output_image_path, max_size_kb=1024):
    image = Image.open(input_image_path).convert("RGB")
    image.save(output_image_path, format="PNG", optimize=True, quality=85)

    while os.path.getsize(output_image_path) > max_size_kb * 1024:
        image = Image.open(output_image_path)
        image.save(output_image_path, format="PNG", optimize=True, quality=85)

@app.on_message(filters.command("img_to_base64"))
@capture_err
async def img_to_base64_command(_, message: Message):
    if len(message.command) == 1:  # Only the command is provided
        return await message.reply("Usage: Reply to an image with the command `/img_to_base64` to convert it to Base64.")
    
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("Please reply to an image to convert it to Base64.")
    
    process_message = await message.reply_text("Downloading image...")

    photo = message.reply_to_message.photo
    original_image_path = await photo.download()

    if os.path.getsize(original_image_path) > 1024 * 1024:  # 1 MB
        os.remove(original_image_path)
        return await process_message.edit_text("Image size exceeds 1 MB. Please send an image within 1 MB.")

    await process_message.edit_text("Compressing image...")

    compressed_image_path = "compressed_image.png"
    compress_image(original_image_path, compressed_image_path)

    await process_message.edit_text("Converting image to Base64...")

    base64_string = image_to_base64(compressed_image_path)
    data_uri = f"data:image/png;base64,{base64_string}"
    
    result_text = f"Base64:\n{base64_string}\n\nData URI:\n{data_uri}"

    # Delete original and compressed images
    os.remove(original_image_path)
    os.remove(compressed_image_path)

    # Check if result exceeds message limit (4096 characters for Telegram)
    if len(result_text) > 4096:
        timestamp = int(time.time())
        result_file_path = f"img_to_base64_result_{timestamp}.txt"
        with open(result_file_path, "w") as result_file:
            result_file.write(result_text)
        
        await process_message.delete()
        await message.reply_document(result_file_path, caption="Here’s your image converted to Base64.")
        os.remove(result_file_path)
    else:
        await process_message.edit_text(f"Here’s your image converted to Base64:\n```\n{result_text}\n```", parse_mode="Markdown")

@app.on_message(filters.command("base64_to_img"))
@capture_err
async def base64_to_img_command(_, message: Message):
    if len(message.command) == 1:  # Only the command is provided
        return await message.reply("Usage: Reply to a text file containing Base64 with the command `/base64_to_img`, or provide a Base64 string directly.")

    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document
        if not document.mime_type == "text/plain":
            return await message.reply("Please reply to a text file containing Base64 string.")
        
        process_message = await message.reply_text("Downloading Base64 text file...")

        # Check if file size is within 1 MB
        if document.file_size > 1024 * 1024:
            return await process_message.edit_text("The text file size exceeds 1 MB. Please send a file within 1 MB.")
        
        base64_file_path = await document.download()
        with open(base64_file_path, "r") as base64_file:
            base64_string = base64_file.read().strip()
        os.remove(base64_file_path)
    else:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.reply("Please provide a Base64 string to convert to an image.")
        base64_string = args[1].strip()

    try:
        await process_message.edit_text("Converting Base64 to image...")

        image_bytes = base64.b64decode(base64_string)
        image_path = "output_image.png"
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        
        await process_message.delete()
        await message.reply_photo(photo=image_path, caption="Here’s your Base64 converted to an image.")
        os.remove(image_path)
    except (base64.binascii.Error, UnicodeDecodeError):
        await process_message.edit_text("Invalid Base64 string. Please provide a valid Base64 encoded string.")