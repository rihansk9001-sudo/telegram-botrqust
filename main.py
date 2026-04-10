from flask import Flask
import threading
import os
import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ---------------------------
#   WEB SERVER (IMPORTANT)
# ---------------------------
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running on Render Web Service!"

def run_flask():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()


# ---------------------------
#   TELEGRAM BOT SETTINGS
# ---------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client("admin_add_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)


# ---------------------------
#   START MESSAGE
# ---------------------------
@app.on_message(filters.command("start") & filters.private)
async def start(_, msg):
    me = await app.get_me()
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("➕ Add Me As Admin", url=f"tg://resolve?domain={me.username}")]]
    )

    await msg.reply(
        "**👋 Namaste!**\n\n"
        "👉 Mujhe jis channel me kaam karna hai, waha **Admin** bana do.\n\n"
        "Admin dene ke liye niche button dabao:",
        reply_markup=btn
    )


# ---------------------------
#   LIST CHANNELS
# ---------------------------
@app.on_message(filters.command("channels") & filters.private)
async def list_channels(_, msg):
    dialogs = await app.get_dialogs()
    buttons = []

    for d in dialogs:
        if d.chat.type in [enums.ChatType.CHANNEL, enums.ChatType.SUPERGROUP]:
            buttons.append(
                [InlineKeyboardButton(d.chat.title, callback_data=f"set_{d.chat.id}")]
            )

    await msg.reply("📢 **Select your Channel:**", reply_markup=InlineKeyboardMarkup(buttons))


# ---------------------------
#   SET CHANNEL
# ---------------------------
@app.on_callback_query(filters.regex("set_"))
async def set_channel(_, query):
    chat_id = int(query.data.split("_")[1])
    await query.message.edit(
        f"✅ Channel Set: `{chat_id}`\n\n"
        "**Channel me jao aur ye command bhejo:**\n"
        "`/allaccept`"
    )


# ---------------------------
#   ACCEPT ALL REQUESTS
# ---------------------------
@app.on_message(filters.command("allaccept"))
async def accept_requests(_, msg):
    chat_id = msg.chat.id

    try:
        async for req in app.get_chat_join_requests(chat_id):
            await app.approve_chat_join_request(chat_id, req.user.id)

        await msg.reply(
            "🎉 **Saare pending requests approve ho gayi!**\n"
            "❌ Kisi ko dismiss nahi kiya gaya."
        )

    except Exception as e:
        await msg.reply(f"⚠️ Error: `{e}`\n👉 Mujhe admin permissions check karo.")


print("Bot Running...")
app.run()
