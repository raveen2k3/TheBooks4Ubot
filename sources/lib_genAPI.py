from libgen_api import LibgenSearch
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , InlineQueryResultArticle, InputTextMessageContent
from configs import *

@Rias.on_message(filters.command(["search"]))
async def search(client , message):
  m=message.command
  if len(m)==1:
    return await message.reply("❌ **Enter Your Bookname AlongSide With Command !**")

  t=await message.reply("`Searching this book...`")
  name=message.from_user.first_name
  bookname=" ".join(m[1:])
  global s
  s = LibgenSearch()
  global results
  results = s.search_title(bookname)
  global l
  l=len(results)
  if l==0:
    return await t.edit_text("❌ **BOOK NOT FOUND**")
  #print(bookname)
  global i
  i = 0
  item_to_download = results[i]
  download_links = s.resolve_download_links(item_to_download)
    
  data_text = "✅ **Title:** `" + results[i]['Title'] +"`\n\n✍️ **Author:** " + results[i]['Author'] + "\n**🎙️ Language:** " + results[i]['Language'] + "\n🔰 **published on:** " + results[i]['Year'] + "\n🔰 **Size:** " + results[i]['Size'] + "\n📑 **Ext:** " + results[i]['Extension']
  data_text=data_text+f"\n❄️ **Requested By:**  [{name}](tg://user?id={str(message.from_user.id)})"
  item_to_download = results[i]
  download_links = s.resolve_download_links(item_to_download)

  if l==1:
    await message.reply(data_text , reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Link1" , url=download_links["GET"]) ,
                 InlineKeyboardButton(text="❌", callback_data=f"close|{message.from_user.id}"),
                 InlineKeyboardButton(text="Link2" , url=download_links["Cloudflare"])]
            ]
        )
    )   
  else:  
    await message.reply(data_text , reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Link1" , url=download_links["GET"]) ,
                 InlineKeyboardButton(text="Link2" , url=download_links["Cloudflare"])],
                [InlineKeyboardButton("Next⏩", callback_data=f"next1|{message.from_user.id}|{name}"),
                 InlineKeyboardButton(text="Close ❌", callback_data=f"close|{message.from_user.id}")]
            ]
        )
    )
       
  await t.delete()
  sender_name=message.from_user.first_name
  sender_username=message.from_user.username
  await Rias.send_message(chat_id=-1001844178222 , text="bookname :"+ bookname +"\n\n" +"requested by :" + sender_name + " " +"\n\nSender Username : "+ "@" +sender_username  + " " + "\n\nSender ID : " + str(message.from_user.id))
  
@Rias.on_inline_query(filters.regex(r"^(?P<input>[\S ]+)$") )
async def answer(client, inline_query):
    bookname=inline_query.matches[0].group('input')
    print(bookname)
    find = LibgenSearch()
    result = find.search_title(bookname)
    item_to_download = result[0]
    download_links = find.resolve_download_links(item_to_download)
    name=inline_query.from_user.first_name
    data_text = "✅ **Title:** `" + result[0]['Title'] +"`\n\n✍️ **Author:** " + result[0]['Author'] + "\n**🎙️ Language:** " + result[0]['Language'] + "\n🔰 **published on:** " + result[0]['Year'] + "\n🔰 **Size:** " + result[0]['Size'] + "\n📑 **Ext:** " + result[0]['Extension']
    data_text=data_text+f"\n❄️ **Requested By:**  [{name}]" 
    item_to_download = result[0]
    
    item_to_download1 = result[1]
    download_links1 = find.resolve_download_links(item_to_download1)
    name1=inline_query.from_user.first_name
    data_text1 = "✅ **Title:** `" + result[1]['Title'] +"`\n\n✍️ **Author:** " + result[1]['Author'] + "\n**🎙️ Language:** " + result[1]['Language'] + "\n🔰 **published on:** " + result[1]['Year'] + "\n🔰 **Size:** " + result[1]['Size'] + "\n📑 **Ext:** " + result[1]['Extension']
    data_text1=data_text1+f"\n❄️ **Requested By:**  [{name1}]" 
    
    item_to_download2 = result[2]
    download_links2 = find.resolve_download_links(item_to_download2)
    name1=inline_query.from_user.first_name
    data_text2 = "✅ **Title:** `" + result[2]['Title'] +"`\n\n✍️ **Author:** " + result[2]['Author'] + "\n**🎙️ Language:** " + result[2]['Language'] + "\n🔰 **published on:** " + result[2]['Year'] + "\n🔰 **Size:** " + result[2]['Size'] + "\n📑 **Ext:** " + result[2]['Extension']
    data_text2=data_text2+f"\n❄️ **Requested By:**  [{name1}]" 
    
    

    support_text = "Join @BakaForum For buf fixes and Suggestions\n\n Join By clicking Below Button"
    try:
        await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        title=result[0]['Title'],
                        input_message_content=InputTextMessageContent(
                            data_text,
                        ),
                        description="Got Your Books Press This Button To Download",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    "Link1",
                                    url=download_links["GET"]
                                )],
                                [InlineKeyboardButton(
                                    "Link2",
                                    url=download_links["Cloudflare"]
                                )]
                            ]
                        )
                    ),
                    InlineQueryResultArticle(
                        title=result[1]['Title'],
                        input_message_content=InputTextMessageContent(
                            data_text1
                        ),
                        description="Got Your Books Press This Button To Download",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    "Link1",
                                    url=download_links1["GET"]
                                )],
                                [InlineKeyboardButton(
                                    "Link2",
                                    url=download_links1["Cloudflare"]
                                )]
                            ]
                        )
                    ),
                    InlineQueryResultArticle(
                        title=result[2]['Title'],
                        input_message_content=InputTextMessageContent(
                            data_text2
                        ),
                        description="Got Your Books Press This Button To Download",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    "Link1",
                                    url=download_links2["GET"]
                                )],
                                [InlineKeyboardButton(
                                    "Link2",
                                    url=download_links2["Cloudflare"]
                                )]
                            ]
                        )
                    ),
                    InlineQueryResultArticle(
                        title="Support",
                        input_message_content=InputTextMessageContent(
                            support_text
                        ),
                        url="https://telegram.me/BakaForum",
                        description="join Us :-) ",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    "JOIN US",
                                    url="https://telegram.me/BakaForum"
                                )]
                            ]
                        )
                    )
                ],
                cache_time=2
            )
    except:
        await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title=result[0]['Title'],
                input_message_content=InputTextMessageContent(
                    data_text,
                ),
                description="Got Your Books Press This Button To Download",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "Link1",
                            url=download_links["GET"]
                        )],
                        [InlineKeyboardButton(
                            "Link2",
                            url=download_links["Cloudflare"]
                        )]
                    ]
                )
            ),
                    InlineQueryResultArticle(
                        title="Support",
                        input_message_content=InputTextMessageContent(
                            support_text
                        ),
                        url="https://telegram.me/BakaForum",
                        description="join Us :-) ",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    "JOIN US",
                                    url="https://telegram.me/BakaForum"
                                )]
                            ]
                        )
                    )
                ],
                cache_time=2
            )
        







        
@Rias.on_callback_query(filters.regex("next"))
async def next_things(Rias, query):
      d=query.data.split("|")
      uid=d[1]
      nem=d[2]
      num=int(d[0].replace("next", ""))
      if query.from_user.id != int(uid):
        #if query.from_user.id not in OWNER+db.get_admin():
          try:
            return await query.answer(
              "❌ You Cant access This!\nSearch your own book.", show_alert=True
              )
          except:
            return 

      if l-1==num:
        await query.answer()
        data_text = "✅ **Title:** `" + results[i+num]['Title'] +"`\n\n✍️ **Author:** " + results[i+num]['Author'] + "\n**🎙️ Language:** " + results[i+num]['Language'] + "\n🔰 **published on:** " + results[i+num]['Year'] + "\n🔰 **Size:** " + results[i+num]['Size'] + "\n📑 **Ext:** " + results[i+num]['Extension']
        data_text=data_text+f"\n❄️ **Requested By:**  [{nem}](tg://user?id={uid})"
        item_to_download = results[i+num]
        download_links = s.resolve_download_links(item_to_download)
        await query.message.edit_text(text=data_text, reply_markup =InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Link1" , url=download_links["GET"]) ,
             InlineKeyboardButton(text="Link2" , url=download_links["Cloudflare"])],
            [InlineKeyboardButton("Back⏪" , callback_data=f"next{str(num-1)}|{uid}|{nem}"),
             InlineKeyboardButton(text="Close ❌", callback_data=f"close|{uid}")]]
                                                      ))
    
      elif num==0:
        await query.answer()
        data_text = "✅ **Title:** `" + results[0]['Title'] +"`\n\n✍️ **Author:** " + results[0]['Author'] + "\n**🎙️ Language:** " + results[0]['Language'] + "\n🔰 **published on:** " + results[0]['Year'] + "\n🔰 **Size:** " + results[0]['Size'] + "\n📑 **Ext:** " + results[0]['Extension']
        data_text=data_text+f"\n❄️ **Requested By:**  [{nem}](tg://user?id={uid})"
        item_to_download = results[0]
        download_links = s.resolve_download_links(item_to_download)
        await query.message.edit_text(text= data_text, reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Link1" , url=download_links["GET"]) ,
                 InlineKeyboardButton(text="Link2" , url=download_links["Cloudflare"])],
                [InlineKeyboardButton("Next⏩", callback_data=f"next1|{uid}|{nem}"),
                 InlineKeyboardButton(text="Close ❌", callback_data=f"close|{uid}")]]
                                ))
        
      else:
        await query.answer()
        data_text = "✅ **Title:** `" + results[i+num]['Title'] +"`\n\n✍️ **Author:** " + results[i+num]['Author'] + "\n**🎙️ Language:** " + results[i+num]['Language'] + "\n🔰 **published on:** " + results[i+num]['Year'] + "\n🔰 **Size:** " + results[i+num]['Size'] + "\n📑 **Ext:** " + results[i+num]['Extension']
        data_text=data_text+f"\n❄️ **Requested By:**  [{nem}](tg://user?id={uid})"
        item_to_download = results[i+num]
        download_links = s.resolve_download_links(item_to_download)
        await query.message.edit_text(text=data_text, reply_markup =InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Link1" , url=download_links["GET"]) ,
             InlineKeyboardButton(text="Link2" , url=download_links["Cloudflare"])],
            [InlineKeyboardButton("⏪" , callback_data=f"next{str(num-1)}|{uid}|{nem}"),
             InlineKeyboardButton(text="❌", callback_data=f"close|{uid}"),
             InlineKeyboardButton("⏩" , callback_data=f"next{str(num+1)}|{uid}|{nem}")]]
                                                      ))
 
    


@Rias.on_callback_query(filters.regex("close"))
async def close_buttom(Rias, query):
    d=query.data.split("|")
    uid=d[1]
    if query.from_user.id != int(uid):
      #if query.from_user.id not in OWNER+db.get_admin():
        try:
          return await query.answer(
            "❌ This buttoms is not for you!\nSearch your own book.", show_alert=True
            )
        except:
          return 
    await query.message.delete()        
     
             



@Rias.on_callback_query(filters.regex("About"))
async def close_buttom(Rias, query):        
    await query.answer()
    await query.message.edit_text(
        text=f"**Welcome !!."
             "\nHere is a detailed guide to use me."
             "\n\nuse /search <your bookname> ill grab you the direct download links."
             "\n\nyou might had difficulty , in Searching before , we are here to solve it :-) ."
             "\n\nFor further information and guidance contact my developers at my support group.**",
             reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/BakaForum"),
                ]
            ]
        )
        )
