import config
from utils.qrcode import generate
from utils.vpn import Outline
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from pyromod import listen
from outline_vpn.outline_vpn import OutlineKey

try:
    outline = Outline()
except:
    print("Variables is incorrect !")

try:
    client = Client(name=config.CONFIG_START_NAME,
                    api_id=config.API_ID_TELEGRAM,
                    api_hash=config.API_HASH_TELEGRAM,
                    bot_token=config.BOT_TOKEN_TELEGRAM)
except:
    print("Variables is incorrect !")



def users_list():
    markup = []
    row = []
    for key in outline.get_keys():
        try:
            
            name = key.name
            if name == "":
                name = "no-name"
            button = InlineKeyboardButton(name, f"user_{key.key_id}")
            row.append(button)

            if len(row) == 3:
                markup.append(row)
                row = []

        except Exception as e:
            print(f"Error: {e}")
            continue

    if row:
        markup.append(row)
    return InlineKeyboardMarkup(markup)

def query_filter(callback: CallbackQuery, data):
    return callback.data == data

def delete_markup(key_id):

    markup = InlineKeyboardMarkup([

        [
            InlineKeyboardButton("حذف ⛔", f"delete_{key_id}"),
            InlineKeyboardButton("بازگشت", "back_delete"),
            ],

    ])

    return markup
cancel_markup = InlineKeyboardMarkup([

    [
        InlineKeyboardButton("منصرف", "cancel"),
        ],

])

back_markup = InlineKeyboardMarkup([

    [
        InlineKeyboardButton("بازگشت", "back"),
    ],

])

panel_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("• ساخت سرویس", "key_create")
        
    ],
    [
        InlineKeyboardButton("• مدیریت سرویس ها", "keys_list"), 
    #    InlineKeyboardButton("• ویرایش سرویس", "key_edit"),
    #    InlineKeyboardButton("• حذف سرویس", "key_delete")
    ],
    [
        InlineKeyboardButton("• اطلاعات سرور", "server_info"),
        InlineKeyboardButton("• ویرایش سرور", "server_edit")
    ]])


@client.on_message(filters.command("start") & filters.user(config.ADMIN_ID), group=2)
async def handle(client: Client, message: Message):
    await message.reply(
        text="لطفا یکی از دکمه های زیر را انتخاب کنید 👇",
        reply_markup=panel_markup)

@client.on_callback_query(group=0)
async def handlers(client: Client, callback: CallbackQuery):
    if query_filter(callback, "keys_list"):


        await callback.message.reply("**لیست سرویس های ربات :**", reply_markup=users_list())



@client.on_callback_query(filters.user(config.ADMIN_ID), group=1)
async def handler(client: Client, callback: CallbackQuery):
    if query_filter(callback, "key_create"):
        limit = await client.ask(chat_id=callback.message.chat.id, text="حجم مورد نظر را برای سرویس ارسال کنید\n برای حجم نامحدود عدد 0 را ارسال کنید", reply_markup=back_markup)

        if int(limit.text) != 0:
            key = outline.create_key(int(limit.text))
        else:
            key = outline.create_key()
        await client.delete_messages(limit.chat.id, limit.id)
        
        await client.send_photo(callback.message.chat.id, generate(f"{key.access_url}#{key.name}"), f"**لینک سرویس شما ایجاد شد!**\nلینک: \n`{key.access_url}#{key.name}`", reply_to_message_id=callback.message.id, parse_mode=ParseMode.MARKDOWN)
        

@client.on_callback_query(filters.user(config.ADMIN_ID), group=3)
async def handler(client: Client, callback: CallbackQuery):
    if callback.data.startswith("user_"):
        key_id = callback.data.replace("user_", "")
        key = outline.get_key(key_id)
        text = f"""
نام سرویس : {key.name}
شناسه سرویس : {key.key_id}
محدودیت حجمی : {key.data_limit}
حجم استفاده شده : {key.used_bytes}
لینک سرویس : 
`{key.access_url}#{key.name}`
"""
        await client.send_photo(callback.message.chat.id, generate(f"{key.access_url}#{key.name}"), text, reply_markup=delete_markup(key_id))
        await callback.message.delete()
    elif callback.data.startswith("delete_"):
        key_id = callback.data.replace("delete_", "")
        outline.delete_key(key_id)
        await callback.edit_message_text("**سرویس مورد نظر حذف شد !**", reply_markup=back_markup)

    


@client.on_callback_query(filters.user(config.ADMIN_ID), group=4)
async def handler(client: Client, callback: CallbackQuery):
    if callback.data == "back_delete":
        await callback.message.delete()
        await callback.message.edit_text("**لیست سرویس های ربات :**", reply_markup=users_list())

    if callback.data == "back":
        await callback.message.delete()
        await callback.message.edit_text("لطفا یکی از دکمه های زیر را انتخاب کنید 👇", reply_markup=panel_markup)
    elif callback.data == "cancel":
        await callback.message.delete()

            
            




client.run()