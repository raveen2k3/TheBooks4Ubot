from pyrogram import Client
API_ID = int(" ")
API_HASH = " "
BOT_TOKEN = " "
DB_URL = " "
DB_NAME =" "
ownerId = int(1871813121) #replace your id here
MAX_MESSAGE_LENGTH = 4096

Rias = Client("Rias",api_id=API_ID , api_hash=API_HASH ,bot_token=BOT_TOKEN ,plugins={"root": "sources"})
