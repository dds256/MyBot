from pyrogram import filters
from pyrogram.types import Message
from AKDBOT import app
from AKDBOT.utils.errors import capture_err

def decimal_to_hex(decimal_number):
    hex_value = hex(decimal_number)
    return hex_value

@app.on_message(filters.command("dec2hex"))
@capture_err
async def hex_converter_command(_, message: Message):
    if message.reply_to_message:
        input_text = message.reply_to_message.text.strip()
    else:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.reply("Please provide a decimal number to convert to hex.")
        input_text = args[1].strip()
    
    try:
        decimal_number = int(input_text)
        hex_value = decimal_to_hex(decimal_number)
        choice_prompt = "\nAre you using this for patching Smali? (Y/N)"
        choice_message = await message.reply(choice_prompt)

        @app.on_message(filters.reply & filters.user(message.from_user.id))
        async def choice_handler(client, reply_message: Message):
            choice = reply_message.text.strip().lower()
            if choice == "y":
                hex_value_smali = f"{hex_value}L"
                response = f"Your Hex Value is: `{hex_value}`\nFor Patching Smali use: `{hex_value_smali}`"
            elif choice == "n":
                response = f"Your Hex Value is: `{hex_value}`"
            else:
                response = "Enter a valid choice (Y/N)."
            
            await reply_message.reply(response, parse_mode="Markdown")
            app.remove_handler(choice_handler)
        
    except ValueError:
        await message.reply("Please provide a valid decimal number.")