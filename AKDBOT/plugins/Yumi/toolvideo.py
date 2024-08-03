import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pydub import AudioSegment
from AKDBOT import app

# Constants
MAX_FILE_SIZE_MB = 100
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes

def generate_unique_filename(extension):
    timestamp = int(time.time())
    return f"output_{timestamp}.{extension}"

@app.on_message(filters.command("extract") & filters.reply)
async def extract_media_cmd(client, message: Message):
    process_message = await message.reply_text("Processing...")

    try:
        replied_message = message.reply_to_message

        if replied_message.video:
            if len(message.command) > 1:
                command = message.command[1].lower()
                file_path = await replied_message.download()

                if os.path.getsize(file_path) > MAX_FILE_SIZE_BYTES:
                    os.remove(file_path)
                    await process_message.edit_text("The file size exceeds 100 MB. Please provide a smaller file.")
                    return
                
                if command == "audio":
                    await process_message.edit_text("Extracting audio from video...")
                    audio_path = generate_unique_filename("mp3")
                    audio = AudioSegment.from_file(file_path)
                    audio = audio.set_channels(1)
                    audio.export(audio_path, format="mp3")
                    await client.send_audio(message.chat.id, audio_path)
                    
                    os.remove(file_path)
                    os.remove(audio_path)
                
                elif command == "video":
                    await process_message.edit_text("Extracting video without audio...")
                    video_path = generate_unique_filename("mp4")
                    os.system(f"ffmpeg -i {file_path} -c copy -an {video_path}")
                    await client.send_video(message.chat.id, video_path)
                    
                    os.remove(file_path)
                    os.remove(video_path)
                
                else:
                    await process_message.edit_text("Invalid command. Please use either `/extract audio` or `/extract video`.")
            
            else:
                await process_message.edit_text("Please specify whether to extract audio or video using `/extract audio` or `/extract video`.")
        
        else:
            await process_message.edit_text("The replied message is not a video.")
    
    except Exception as e:
        await process_message.edit_text(f"An error occurred: {str(e)}")
    
    finally:
        # Cleanup if file was not handled or any additional cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)