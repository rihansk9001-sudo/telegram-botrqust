import os
import asyncio
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

@bot.on_message(filters.command("start"))
async def start_cmd(c, m):
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Me As Admin",
                    url=f"https://t.me/{(await c.get_me()).username}?startchannel=true"
                )
            ]
        ]
    )

    await m.reply(
        "👋 Hi! Mujhe admin do, phir /allaccept command use karo.",
        reply_markup=btn
    )

@bot.on_message(filters.command("allaccept"))
async def accept_all(c, m):
    chat_id = m.chat.id

    try:
        pending = c.get_chat_join_requests(chat_id)
        count = 0

        async for req in pending:
            await c.approve_chat_join_request(chat_id, req.user.id)
            count += 1

        await m.reply(f"✅ {count} requests approved!")

    except Exception as e:
        await m.reply(f"❌ Error: `{e}`")

async def start_all():
    await bot.start()
    print("Bot started successfully!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_all())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
