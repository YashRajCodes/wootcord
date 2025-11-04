from . import conversation_created, message_created

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
        # TODO: dispatch to specific handlers based on event type