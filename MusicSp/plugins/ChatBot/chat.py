import os

from openai import AsyncOpenAI
from pyrogram import filters
from pyrogram.types import Message

from MusicSp import app
from MusicSp.plugins.ChatBot.memory import get_memory, save_message
from MusicSp.plugins.ChatBot.settings import is_ai_enabled
from MusicSp.plugins.ChatBot.personality import get_personality


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


@app.on_message(filters.text)
async def ai_chat(client_app, message: Message):

    if not message.text:
        return

    # Ignore commands so music bot commands keep working
    if message.text.startswith(("/", "!", ".")):
        return

    # Ignore messages sent by bots
    if message.from_user and message.from_user.is_bot:
        return

    # Check OpenAI configuration
    if not client:
        return await message.reply_text(
            "⚠️ AI chatbot is not configured yet."
        )

    # Check whether AI chatbot is enabled
    if not await is_ai_enabled():
        return

    # Make sure we have a user
    if not message.from_user:
        return

    user_id = message.from_user.id

    try:
        # Show typing status
        await message.chat.do("typing")

        # Get user's saved conversation
        history = await get_memory(
            user_id,
            limit=10,
        )

        # Get current AI personality
        personality = await get_personality()

        # Current user message
        input_messages = history + [
            {
                "role": "user",
                "content": message.text,
            }
        ]

        # Ask AI
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=personality,
            input=input_messages,
        )

        answer = response.output_text.strip()

        if not answer:
            answer = "Hmm 😅 mujhe iska proper answer nahi mila."

        # Save user message
        await save_message(
            user_id,
            "user",
            message.text,
        )

        # Save AI response
        await save_message(
            user_id,
            "assistant",
            answer,
        )

        # Send AI response
        await message.reply_text(answer)

    except Exception as e:
        print(f"AI ChatBot Error: {e}")

        await message.reply_text(
            "😔 Sorry, abhi AI se response nahi aa raha. "
            "Thodi der baad try karo."
        )
