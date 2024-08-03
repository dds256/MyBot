from pyrogram import Client, filters
from AKDBOT import app
from config import OWNER_ID, BOT_USERNAME
from pyrogram.types import Message

@app.on_message(filters.command(["post"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def copy_messages(_, message: Message):
    # Extract the command and arguments
    command_parts = message.text.split()

    if len(command_parts) < 2:
        await message.reply("Please specify a destination group/user ID.")
        return

    destination_id = command_parts[1]

    if not destination_id.startswith("-100") and not destination_id.startswith("@"):
        await message.reply("Invalid ID. Please use a valid group/user ID.")
        return

    if message.reply_to_message:
        try:
            # Forward the message to the specified destination
            await message.reply_to_message.copy(destination_id)
            await message.reply("Post successful.")
        except Exception as e:
            await message.reply(f"Failed to post: {str(e)}")
    else:
        await message.reply("Please reply to a message to post it.")
        