import re
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from AKDBOT import app
from AKDBOT.utils.errors import capture_err

def date_to_hex(date_str):
    date_format = "%d/%m/%Y"
    date_obj = datetime.strptime(date_str, date_format)
    epoch = datetime(1970, 1, 1)
    seconds_since_epoch = int((date_obj - epoch).total_seconds())
    hex_value = f"0x{seconds_since_epoch:X}L"
    return hex_value

@app.on_message(filters.command("date2hex"))
@capture_err
async def date_to_hex_command(_, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Please provide a date in the format dd/mm/yyyy.")
    
    date_str = args[1].strip()
    try:
        hex_code = date_to_hex(date_str)
        formatted_code = f"```\n{hex_code}\n```\nGhostKiller Thanks for code"
        await message.reply(formatted_code, parse_mode="Markdown")
    except ValueError:
        await message.reply("Invalid date format. Please use dd/mm/yyyy.")

if __name__ == "__main__":
    print("Bot is running...")