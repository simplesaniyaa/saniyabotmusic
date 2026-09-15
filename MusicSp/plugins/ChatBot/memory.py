from MusicSp.core.mongo import mongodb


# Chatbot memory collection
chat_memory = mongodb.chat_memory


async def get_memory(user_id, limit=10):
    """Get recent conversation history of a user."""
    data = await chat_memory.find_one({"user_id": user_id})

    if not data:
        return []

    return data.get("messages", [])[-limit:]


async def save_message(user_id, role, content, limit=20):
    """Save a message to the user's conversation memory."""

    await chat_memory.update_one(
        {"user_id": user_id},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content,
                }
            }
        },
        upsert=True,
    )

    # Keep only the latest messages
    data = await chat_memory.find_one({"user_id": user_id})

    if data and len(data.get("messages", [])) > limit:
        messages = data["messages"][-limit:]

        await chat_memory.update_one(
            {"user_id": user_id},
            {"$set": {"messages": messages}},
        )


async def clear_memory(user_id):
    """Clear a user's chatbot memory."""
    await chat_memory.delete_one({"user_id": user_id})
