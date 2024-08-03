import requests
from AKDBOT import app
from pyrogram import filters

@app.on_message(filters.command("id_faker"))
async def address(client, message):
    user = message.from_user
    query = message.text.split(maxsplit=1)[1].strip() if len(message.text.split(maxsplit=1)) > 1 else "us"
    url = f"https://randomuser.me/api/?nat={query}"
    
    process_message = await message.reply_text("Generating fake identity, please wait...")

    response = requests.get(url)
    data = response.json()

    if "results" in data:
        user_data = data["results"][0]

        name = f"{user_data['name']['title']} {user_data['name']['first']} {user_data['name']['last']}"
        address = f"{user_data['location']['street']['number']} {user_data['location']['street']['name']}" 
        city = user_data['location']['city']
        state = user_data['location']['state']
        country = user_data['location']['country'] 
        postal = user_data['location']['postcode']
        email = user_data['email']
        phone = user_data['phone']
        picture_url = user_data['picture']['large']

        # Additional Information
        username = user_data['login']['username']
        dob = user_data['dob']['date']
        gender = user_data['gender']
        nationality = user_data['nat']
        registered = user_data['registered']['date']
        cell = user_data['cell']
        id_name = user_data['id']['name']
        id_value = user_data['id']['value']

        caption = f"""
**{user.mention}, here's your fake identity:**

**ɴᴀᴍᴇ** ⇢ `{name}`
**ᴀᴅᴅʀᴇss** ⇢ `{address}`
**ᴄᴏᴜɴᴛʀʏ** ⇢ `{country}`
**ᴄɪᴛʏ** ⇢ `{city}`
**sᴛᴀᴛᴇ** ⇢ `{state}`
**ᴘᴏsᴛᴀʟ** ⇢ `{postal}`
**ᴇᴍᴀɪʟ** ⇢ {email}
**ᴘʜᴏɴᴇ** ⇢ {phone}
**ᴜsᴇʀɴᴀᴍᴇ** ⇢ `{username}`
**ᴅᴀᴛᴇ ᴏғ ʙɪʀᴛʜ** ⇢ `{dob}`
**ɢᴇɴᴅᴇʀ** ⇢ `{gender}`
**ɴᴀᴛɪᴏɴᴀʟɪᴛʏ** ⇢ `{nationality}`
**ʀᴇɢɪsᴛᴇʀᴇᴅ** ⇢ `{registered}`
**ᴄᴇʟʟ** ⇢ {cell}
**ID ({id_name})** ⇢ `{id_value}`
        """

        await process_message.delete()
        await message.reply_photo(photo=picture_url, caption=caption)
    else:
        await process_message.delete()
        await message.reply_text("Oops, could not generate a fake identity. Please try again later.")