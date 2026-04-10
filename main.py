import os
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
bot = Client(
    "admin_accept_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.route("/")
def home():
    return "Bot is running on Render Web Service!"

# /start command
@bot.on_message(filters.command("start"))
async def start_cmd(c, m):
    btn = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("➕ Add Me As Admin", url=f"https://t.me/{BOT_USERNAME}?startchannel=true")]
        ]
    )
    await m.reply(
        "**Hi! Mujhe admin banao taki mai pending members accept kar sakun.**",
        reply_markup=btn
    )

# /allaccept command
@bot.on_message(filters.command("allaccept"))
async def accept_all(c, m):
    chat_id = m.chat.id

    try:
        pending = await c.get_chat_join_requests(chat_id)
        count = 0

        async for req in pending:
            await c.approve_chat_join_request(chat_id, req.user.id)
            count += 1

        await m.reply(f"✅ {count} members Approved Successfully!")

    except Exception as e:
        await m.reply(f"❌ Error: {e}")

if __name__ == "__main__":
    bot.start()
    app.run(host="0.0.0.0", port=10000)
