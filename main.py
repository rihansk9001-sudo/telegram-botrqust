import os
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client("admin_add_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.command("start") & filters.private)
async def start(_, msg):
    await msg.reply(
        "**👋 Namaste!**\n\n"
        "👉 Mujhe jis channel me kaam karna hai, waha mujhe **Admin** bana do.\n\n"
        "**Admin dene ke liye niche button dabao:**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("➕ Add As Admin", url="tg://resolve?domain={}".format((await app.get_me()).username))]]
        )
    )


@app.on_message(filters.command("channels") & filters.private)
async def list_channels(_, msg):
    dialogs = await app.get_dialogs()
    buttons = []

    for d in dialogs:
        if d.chat.type in [enums.ChatType.CHANNEL, enums.ChatType.SUPERGROUP]:
            buttons.append([InlineKeyboardButton(d.chat.title, callback_data=f"set_{d.chat.id}")])

    await msg.reply("📢 **Select the Channel:**", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("set_"))
async def set_channel(_, query):
    chat_id = int(query.data.split("_")[1])

    await query.message.edit(
        f"✅ Channel Set: `{chat_id}`\n\n"
        "Agar mujhe admin de diya hai to channel me ye command bhejo:\n\n"
        "**/allaccept**"
    )

    # save for user
    app.set_chat(chat_id)


@app.on_message(filters.command("allaccept"))
async def accept_requests(_, msg):
    chat_id = msg.chat.id

    try:
        async for req in app.get_chat_join_requests(chat_id):
            await app.approve_chat_join_request(chat_id, req.user.id)

        await msg.reply("🎉 **Saare members ki join request approve ho gayi!**\n\n❌ *Kisi ko dismiss nahi kiya gaya.*")

    except Exception as e:
        await msg.reply(f"⚠️ Error: `{e}`\n\n👉 Mujhe admin permissions check karo.")


print("BOT RUNNING…")
app.run()
