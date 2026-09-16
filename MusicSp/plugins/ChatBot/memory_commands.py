from pyrogram import filters
from pyrogram.types import Message

from MusicSp import app
from MusicSp.plugins.ChatBot.memory import clear_memory


@app.on_message(filters.command("clearmemory"))
async def clear_memory_command(client, message: Message):

    if not message.from_user:
        return

    user_id = message.from_user.id

    try:
        await clear_memory(user_id)

        await message.reply_text(
            "🧠✨ Tumhari AI chat memory clear kar di gayi hai.\n\n"
            "Ab hum fresh conversation se start kar sakte hain ❤️"
        )

    except Exception as e:
        print(f"Clear Memory Error: {e}")

        await message.reply_text(
            "❌ Memory clear karte waqt error aa gaya."
        )
