import aiohttp
from pyrogram import filters
from AKDBOT import app as app

# Base URLs for the APIs
AGE_API_URL = "https://api.agify.io"
GENDER_API_URL = "https://api.genderize.io"
NATIONALITY_API_URL = "https://api.nationalize.io"

# Function to get age prediction
async def get_age(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(AGE_API_URL, params={"name": name}) as response:
            if response.status == 200:
                return await response.json()
            return None

# Function to get gender prediction
async def get_gender(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(GENDER_API_URL, params={"name": name}) as response:
            if response.status == 200:
                return await response.json()
            return None

# Function to get nationality prediction
async def get_nationality(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(NATIONALITY_API_URL, params={"name": name}) as response:
            if response.status == 200:
                return await response.json()
            return None

@app.on_message(filters.command("predict"))
async def predict_command(bot, message):
    args = message.command[1:]
    if not args:
        await message.reply("Usage: /predict <name>")
        return

    # Join all arguments to form the full name
    name = " ".join(args)
    processing_message = await message.reply("Processing predictions...")

    try:
        age_data = await get_age(name)
        gender_data = await get_gender(name)
        nationality_data = await get_nationality(name)

        if not age_data or not gender_data or not nationality_data:
            await processing_message.edit("Failed to get predictions. Please try again later.")
            return

        age = age_data.get("age", "Unknown")
        gender = gender_data.get("gender", "Unknown")
        nationality_info = nationality_data.get("country", [])
        if nationality_info:
            nationality = ", ".join([country["country_id"] for country in nationality_info])
        else:
            nationality = "Unknown"

        prediction_result = (f"Predictions for the name **{name}**!\n"
                             f"**Age:** {age}\n"
                             f"**Gender:** {gender}\n"
                             f"**Nationality:** {nationality}\n\n"f"By **Muthal Baba**")
        await processing_message.edit(prediction_result)
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")