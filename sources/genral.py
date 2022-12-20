
import io
from pyrogram import filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import pymongo
from configs import ownerId , MAX_MESSAGE_LENGTH ,Rias ,  DB_NAME , DB_URL


def addusertoDb(message):
    my_client = pymongo.MongoClient(DB_URL)
    
    Database = my_client[DB_NAME]
    userid=message.from_user.id
    chat_type = message.chat.type
    collection = Database["users"]
    result = collection.find_one({'userid': userid})

    if result:
        if result.get('userid'): return
        
    username = message.from_user.username
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    
    user = {}
    user['userid'] = userid
    user['chattype'] = str(chat_type)
    user['username'] = username
    user['firstname'] = firstname
    user['lastname'] = lastname

    collection.insert_one(user)

@Rias.on_message(filters.command(["start"]) & filters.private)
async def start(client, message): 
    await message.reply_text(
        text=f"**Hello {message.from_user.first_name} 👋 !"
            "\n\nFeeling Tired of searching your favourite books , we are here to help you. "
            "\n\nCheck About to know the use of me**",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("About", callback_data="About"),
                ]
            ]
        ),
        reply_to_message_id=message.id
    )
    addusertoDb(message)

@Rias.on_message(filters.command(["sh"] ))
async def execution(_, message):
    user_id = message.from_user.id
    if user_id == ownerId:
        status_message = await message.reply_text("Processing ...")
        # DELAY_BETWEEN_EDITS = 0.3
        # PROCESS_RUN_TIME = 100
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_ = message
        if message.reply_to_message:
            reply_to_ = message.reply_to_message

        # start_time = time.time() + PROCESS_RUN_TIME
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "🗿"
        o = stdout.decode()
        if not o:
            o = "🌚"

        OUTPUT = ""
        OUTPUT += f"<b>QUERY:</b>\n<u>Command:</u>\n<code>{cmd}</code> \n"
        OUTPUT += f"<u>PID</u>: <code>{process.pid}</code>\n\n"
        OUTPUT += f"<b>stderr</b>: \n<code>{e}</code>\n\n"
        OUTPUT += f"<b>stdout</b>: \n<code>{o}</code>"

        if len(OUTPUT) > MAX_MESSAGE_LENGTH:
            with io.BytesIO(str.encode(OUTPUT)) as out_file:
                
                out_file.name = "exec.text"
                await reply_to_.reply_document(
                    document=out_file,
                    caption=cmd[: MAX_MESSAGE_LENGTH // 4 - 1],
                    disable_notification=True,
                    quote=True,
                )
        else:
            await reply_to_.reply_text(OUTPUT, quote=True)

        await status_message.delete()
        
@Rias.on_message(filters.command(["guide"]))
async def guide(Rias , message):
    chat_id= message.chat.id
    guide = "Click The Below Guide Button For More Information"
    await Rias.send_message(chat_id , guide , reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Guide", url="https://t.me/BakaForum/3418/4186"),
                InlineKeyboardButton("Support", url="https://t.me/BakaForum")
            ]
        ]
    ))
    
@Rias.on_message(filters.command(["brodcast"]))
async def brodcast (client , message):
    user_id = message.from_user.id
    if user_id == ownerId:
        o = []

        try:
                
            my_client = pymongo.MongoClient(DB_URL)
        
            Database = my_client[DB_NAME]
            userid=message.from_user.id
            collection = Database["users"]
            receivers = [c["userid"] for c in collection.find()]
            for receiver in receivers:
                try:
                    message_to_send = message.reply_to_message.id
                    print(receiver)
                    
                    await Rias.forward_messages(chat_id=receiver, from_chat_id=message.chat.id , message_ids=message_to_send)
                except:
                    o.append(receiver)
                    await Rias.send_message(chat_id=ownerId, text="brodcast failed to " + str(o))
                    continue
                
                
        except Exception as e:
            
            error_msg = str(e)
            await Rias.send_message(chat_id=ownerId, text=error_msg)

donate_sus = "https://graph.org/file/1d609c5089ef2c1a7e6be.mp4"
@Rias.on_message(filters.command(["donate"]))
async def donate(client, message):
    chat_id =message.chat.id
    sponsor_msg = """First of All Im Thanking you for using \n\n/donate option
    \n\n Due To The Poor Server We Have In Our Hand We cant Provide You Better Service
    \n\n It would be be a great help if You Can Help Us To Improve Our Server
    \n\n you can use sponsor button by clicking below
    \n\n feel free to msg in group for alternative Payment Method :-)
    \n\n Anyways this Service will always be free And we Wont force You to pay us"""
    
    await Rias.send_animation(chat_id, animation=donate_sus ,caption=sponsor_msg , reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Support", url="https://telegram.me/BakaForum"),
                    InlineKeyboardButton(text="Donate" , url="https://github.com/sponsors/raveen2k3") ,
                    
                    


                ]
            ]
        )
    )

