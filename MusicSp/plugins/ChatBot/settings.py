from MusicSp.core.mongo import mongodb


chat_settings = mongodb.chat_settings


async def is_ai_enabled():
    """Check whether AI chatbot is enabled."""
    data = await chat_settings.find_one({"_id": "ai_status"})

    if not data:
        return True

    return data.get("enabled", True)


async def set_ai_enabled(enabled: bool):
    """Enable or disable AI chatbot."""
    await chat_settings.update_one(
        {"_id": "ai_status"},
        {
            "$set": {
                "enabled": enabled
            }
        },
        upsert=True,
    )
