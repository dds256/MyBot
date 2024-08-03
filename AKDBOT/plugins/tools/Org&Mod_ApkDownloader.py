import re
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message
from AKDBOT import app

# ------------------------------------

def extract_package_name(play_store_link):
    match = re.search(r'id=([\w.]+)', play_store_link)
    return match.group(1) if match else None

def scrape_original_apk(search_term):
    package_name = extract_package_name(search_term)
    if package_name:
        search_term = package_name
    
    search_engines = [
        ("APKMirror", f"https://www.apkmirror.com/?s={search_term.replace(' ', '+')}"),
        ("APKMonk", f"https://www.apkmonk.com/search/?search={search_term.replace(' ', '+')}")
    ]

    for site_name, url in search_engines:
        response = requests.get(url)
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if site_name == "APKMirror":
            for link in soup.find_all('a', class_='card-link'):
                href = link.get('href')
                if href and href.startswith('/apk/'):
                    download_page_url = f"https://www.apkmirror.com{href}"
                    download_page_response = requests.get(download_page_url)
                    if download_page_response.status_code == 200:
                        download_soup = BeautifulSoup(download_page_response.text, 'html.parser')
                        download_button = download_soup.find('a', {'id': 'downloadButton'})
                        if download_button:
                            return download_button.get('href')
        
        elif site_name == "APKMonk":
            for link in soup.find_all('a', class_='apk-title'):
                href = link.get('href')
                if href:
                    download_page_url = href
                    download_page_response = requests.get(download_page_url)
                    if download_page_response.status_code == 200:
                        download_soup = BeautifulSoup(download_page_response.text, 'html.parser')
                        download_button = download_soup.find('a', {'class': 'btn-download'})
                        if download_button:
                            return download_button.get('href')
    
    return None

def scrape_mod_apk(search_term):
    search_engines = [
        ("Moddroid", f"https://www.moddroid.com/search?q={search_term.replace(' ', '+')}"),
        ("ModYolo", f"https://www.modyolo.com/search?query={search_term.replace(' ', '+')}")
    ]

    for site_name, url in search_engines:
        response = requests.get(url)
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if site_name == "Moddroid":
            for link in soup.find_all('a', class_='download-button'):
                href = link.get('href')
                if href:
                    return href
        
        elif site_name == "ModYolo":
            for link in soup.find_all('a', class_='download-link'):
                href = link.get('href')
                if href:
                    return href
    
    return None

@app.on_message(filters.command("get_apk") & filters.reply)
async def get_apk_command(client, message: Message):
    user = message.from_user.mention
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        return await message.reply("Usage: /get_apk <app_name or Play Store link>")
    
    search_term = args[1].strip()
    await message.reply("Processing your request, please wait...")
    
    download_link = scrape_original_apk(search_term)
    
    if not download_link:
        download_link = scrape_mod_apk(search_term)
    
    if download_link:
        # Send a message with a preview of the APK download link
        await message.reply(f"Here's your APK file: {download_link}\n\nRequested by {user}")
    else:
        await message.reply("Sorry, APK not found.")
    
    await message.delete()

@app.on_message(filters.command("get_apk") & ~filters.reply)
async def get_apk_command_direct(client, message: Message):
    user = message.from_user.mention
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        return await message.reply("Usage: /get_apk <app_name or Play Store link>")
    
    search_term = args[1].strip()
    await message.reply("Processing your request, please wait...")
    
    download_link = scrape_original_apk(search_term)
    
    if not download_link:
        download_link = scrape_mod_apk(search_term)
    
    if download_link:
        # Send a message with a preview of the APK download link
        await message.reply(f"Here's your APK file: {download_link}\n\nRequested by {user}")
    else:
        await message.reply("Sorry, APK not found.")
    
    await message.delete()

@app.on_message(filters.command("get_mod") & filters.reply)
async def get_mod_command(client, message: Message):
    user = message.from_user.mention
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        return await message.reply("Usage: /get_mod <mod_name>")
    
    search_term = args[1].strip()
    await message.reply("Processing your request, please wait...")
    
    download_link = scrape_mod_apk(search_term)
    
    if download_link:
        # Send a message with a preview of the mod APK download link
        await message.reply(f"Here's your mod APK file: {download_link}\n\nRequested by {user}")
    else:
        await message.reply("Sorry, mod APK not found.")
    
    await message.delete()

@app.on_message(filters.command("get_mod") & ~filters.reply)
async def get_mod_command_direct(client, message: Message):
    user = message.from_user.mention
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        return await message.reply("Usage: /get_mod <mod_name>")
    
    search_term = args[1].strip()
    await message.reply("Processing your request, please wait...")
    
    download_link = scrape_mod_apk(search_term)
    
    if download_link:
        # Send a message with a preview of the mod APK download link
        await message.reply(f"Here's your mod APK file: {download_link}\n\nRequested by {user}")
    else:
        await message.reply("Sorry, mod APK not found.")
    
    await message.delete()