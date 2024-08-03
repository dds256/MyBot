import aiohttp
from aiohttp import ContentTypeError
from pyrogram import filters
from AKDBOT import app as app

# Function to generate a random email address
async def generate_random_mailbox():
    url = 'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False, f"HTTP Error: {response.status}"
            try:
                emails = await response.json()
                return True, emails[0]
            except ContentTypeError:
                return False, "Failed to parse response"

@app.on_message(filters.command("generate_email"))
async def generate_email(bot, message):
    success, result = await generate_random_mailbox()
    if not success:
        return await message.reply(f"Failed to generate email: {result}")
    await message.reply(f"Generated Email: `{result}`")

# Function to get messages in a mailbox
async def get_messages(email):
    username, domain = email.split('@')
    url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False, f"HTTP Error: {response.status}"
            try:
                messages = await response.json()
                return True, messages
            except ContentTypeError:
                return False, "Failed to parse response"

@app.on_message(filters.command("check_mailbox"))
async def check_mailbox(bot, message):
    args = message.command[1:]
    if not args:
        return await message.reply("Usage: /check_mailbox <email_address>")
    
    email = args[0]
    success, messages = await get_messages(email)
    if not success:
        return await message.reply(f"Failed to check mailbox: {messages}")

    if not messages:
        return await message.reply("No messages found.")

    reply_text = ""
    for msg in messages:
        reply_text += (
            f"ID: `{msg['id']}`\n"
            f"From: `{msg['from']}`\n"
            f"Subject: `{msg['subject']}`\n"
            f"Date: `{msg['date']}`\n\n"
        )
    await message.reply(reply_text)

# Function to read a specific message
async def read_message(email, message_id):
    username, domain = email.split('@')
    url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={message_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False, f"HTTP Error: {response.status}"
            try:
                message = await response.json()
                return True, message
            except ContentTypeError:
                return False, "Failed to parse response"

@app.on_message(filters.command("read_message"))
async def read_message_command(bot, message):
    args = message.command[1:]
    if len(args) < 2:
        return await message.reply("Usage: /read_message <email_address> <message_id>")

    email = args[0]
    message_id = args[1]
    success, msg = await read_message(email, message_id)
    if not success:
        return await message.reply(f"Failed to read message: {msg}")

    # Ensure we handle missing 'textBody' and 'htmlBody' fields gracefully
    body = msg.get('textBody', '') or msg.get('htmlBody', 'No body found.')

    # Handle attachments
    attachments_info = ''
    if 'attachments' in msg and msg['attachments']:
        attachments_info = '\nAttachments:\n'
        for attachment in msg['attachments']:
            attachments_info += (
                f"Filename: `{attachment['filename']}`\n"
                f"Content Type: `{attachment['contentType']}`\n"
                f"Size: `{attachment['size']}` bytes\n"
            )

    reply_text = (
        f"From: `{msg['from']}`\n"
        f"Subject: `{msg['subject']}`\n"
        f"Date: `{msg['date']}`\n\n"
        f"Body: `{body}`\n"
        f"{attachments_info}"
    )
    await message.reply(reply_text)

# Help command to provide usage details
@app.on_message(filters.command("email_help"))
async def email_help(bot, message):
    help_text = (
        "Here are the available email commands:\n\n"
        "/generate_email - Generates a random email address.\n"
        "Response: `Generated Email: <random_email@domain.com>`\n\n"
        "/check_mailbox <email_address> - Checks the mailbox of the given email address.\n"
        "Response: List of messages in the mailbox.\n"
        "Example: `ID: 639\nFrom: someone@example.com\nSubject: Some subject\nDate: 2018-06-08 14:33:55`\n\n"
        "/read_message <email_address> <message_id> - Reads a specific message from the given email address and message ID.\n"
        "Response: Message content.\n"
        "Example: `From: someone@example.com\nSubject: Some subject\nDate: 2018-06-08 14:33:55\nBody: Some message body`\n"
    )
    await message.reply(help_text)
    