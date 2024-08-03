from io import BytesIO
from os import path, remove
from time import time

from pydub import AudioSegment
from pyrogram import filters
from pyrogram.types import Message

from AKDBOT import app
from AKDBOT.utils.errors import capture_err

from AKDBOT.core.sections import section

async def get_audio_duration(file_path: str) -> float:
    try:
        audio = AudioSegment.from_file(file_path)
        duration = len(audio) / 1000.0  # Duration in seconds
        return duration
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 0

async def convert_audio_to_ogg(input_path: str, output_path: str, max_size_kb: int):
    try:
        audio = AudioSegment.from_file(input_path)
        bitrate = 192  # Start with a reasonable bitrate in kbps

        while bitrate >= 32:  # Minimum bitrate in kbps
            audio.export(output_path, format="ogg", codec="libopus", bitrate=f"{bitrate}k")
            
            if path.getsize(output_path) <= max_size_kb * 1024:
                return True
            
            bitrate -= 8  # Decrease bitrate to reduce file size

        return False
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

async def convert(
    main_message: Message,
    reply_messages,
    status_message: Message,
    start_time: float,
):
    m = status_message

    documents = []
    processing_message = await m.edit("Processing files...")

    for message in reply_messages:
        if not message.audio:
            await m.edit("Not a valid audio document, ABORTED!")
            return

        if message.audio.file_size > 20000000:
            await m.edit("Size too large, sorry babe!")
            return

        file_path = await message.download()
        duration = await get_audio_duration(file_path)

        if duration > 900:
            await m.edit("Audio file duration exceeds 15 minutes, I'm sorry baby!")
            remove(file_path)
            return

        documents.append(file_path)

    conversion_message = await m.edit("Converting audio files...")

    converted_documents = []
    for audio_path in documents:
        output_path = f"{path.splitext(audio_path)[0]}_output.ogg"
        success = await convert_audio_to_ogg(audio_path, output_path, 1000)
        if not success:
            await m.edit("Couldn't compress the audio to fit the size limit, sorry!")
            return
        
        converted_documents.append(output_path)

    elapsed = round(time() - start_time, 2)

    for audio_path in converted_documents:
        sent_message = await main_message.reply_document(
            document=audio_path,
        )
        await sent_message.reply(
            caption=section(
                "Audio to voice",
                body={
                    "Title": path.basename(audio_path),
                    "Size": f"{path.getsize(audio_path) / (10 ** 6):.2f} MB",
                    "Took": f"{elapsed}s",
                },
            ),
        )

    await m.delete()
    await processing_message.delete()
    await conversion_message.delete()

    # Clean up temporary files
    for file in documents + converted_documents:
        if path.exists(file):
            remove(file)

@app.on_message(filters.command("2voice"))
@capture_err
async def audio_to_ogg(_, message: Message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply(
            "Reply to an audio file or group of audio files."
        )

    m = await message.reply_text("Preparing to convert...")
    start_time = time()

    if reply.media_group_id:
        messages = await app.get_media_group(
            message.chat.id,
            reply.id,
        )
        return await convert(message, messages, m, start_time)

    return await convert(message, [reply], m, start_time)