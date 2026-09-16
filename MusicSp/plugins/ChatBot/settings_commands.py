from pyrogram import filters
from pyrogram.types import Message

from MusicSp import app
from MusicSp.plugins.ChatBot.settings import set_ai_enabled
from config import OWNER_ID


@app.on_message(filters.command("aion"))
async def ai_on(client, message: Message):

    if not message.from_user:
        return

    if message.from_user.id != OWNER_ID:
        return await message.reply_text(
            "❌ Sirf bot owner ye command use kar sakta hai."
        )

    await set_ai_enabled(True)

    await message.reply_text(
        "🤖✅ AI Chatbot ON ho gaya!"
    )


@app.on_message(filters.command("aioff"))
async def ai_off(client, message: Message):

    if not message.from_user:
        return

    if message.from_user.id != OWNER_ID:
        return await message.reply_text(
            "❌ Sirf bot owner ye command use kar sakta hai."
        )

    await set_ai_enabled(False)

    await message.reply_text(
        "🤖❌ AI Chatbot OFF ho gaya!"
    )
