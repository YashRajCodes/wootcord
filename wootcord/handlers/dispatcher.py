from . import conversation_created, message_created
from . import discord_message

async def dispatch(bot, data):
    type = data.get("event", "none")

    if type == "none":
        print("Data did not contain an event type, skipping.")
        return
    
    if type == "conversation_created":
        await conversation_created.handle(bot, data)
    elif type == "message_created":
        await message_created.handle(bot, data) 
    else:
        print(f"Received an event of type: {type}")

async def discord_dispatch(bot, type, data):
    print(f"Received Discord event: {type}")
    
    if type == "on_message":
        await discord_message.handler(bot, data)