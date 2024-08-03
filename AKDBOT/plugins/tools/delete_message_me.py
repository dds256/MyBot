from pyrogram import filters
from AKDBOT import app

# Define multiple prefixes for the delete command
DELETE_COMMAND_PREFIXES = ["/", "!", "-"]

# Authorized user IDs
AUTHORIZED_USER_IDS = [1496870437, 6262196413]  # Replace with actual authorized user IDs

# Command to delete a message
@app.on_message(
    filters.command(["delete"], prefixes=DELETE_COMMAND_PREFIXES) & filters.reply
)
async def delete_message(bot, message):
    try:
        # Check if the user is authorized
        if message.from_user.id in AUTHORIZED_USER_IDS:
            # Delete the replied message
            await message.reply_to_message.delete()
            # Delete the command message
            await message.delete()
        else:
            await message.reply_text("You're not authorized to use this command.\n**Derso rupayya lage ga** 💋")
    except Exception as e:
        print("Error deleting message:", e)