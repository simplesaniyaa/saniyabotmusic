from pyrogram import filters
from pyrogram.types import Message

from MusicSp import app
from MusicSp.plugins.ChatBot.personality import (
    set_personality,
    reset_personality,
)
from config import OWNER_ID


@app.on_message(filters.command("prompt"))
async def set_prompt(client, message: Message):

    if not message.from_user:
        return

    if message.from_user.id != OWNER_ID:
        return await message.reply_text(
            "❌ Sirf bot owner ye command use kar sakta hai."
        )

    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ Personality likho.\n\n"
            "Example:\n"
            "/prompt Tum ek friendly aur funny Hinglish AI ho."
        )

    prompt = message.text.split(None, 1)[1].strip()

    await set_personality(prompt)

    await message.reply_text(
        "🎭✅ AI personality successfully update ho gayi!"
    )


@app.on_message(filters.command("resetprompt"))
async def reset_prompt(client, message: Message):

    if not message.from_user:
        return

    if message.from_user.id != OWNER_ID:
        return await message.reply_text(
            "❌ Sirf bot owner ye command use kar sakta hai."
        )

    await reset_personality()

    await message.reply_text(
        "🔄✅ AI personality default par reset ho gayi!"
    )
