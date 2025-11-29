import discord
from wootcord.utils import chatwoot
from wootcord.utils import redis
from wootcord import config

async def handler(bot, message: discord.Message):
    if isinstance(message.channel.parent, discord.ForumChannel) and message.channel.parent.id == config.forum_channel_id:
        payload = chatwoot.convert_dc_message(message)
        conversation_id = await redis.get_conversation_id(message.channel.id)

        if message.webhook_id is not None:
            return  

        if conversation_id is None:
            print(f"No conversation mapping found for Discord thread ID: {message.channel.id}")
            return
        
        try:
            await chatwoot.send_to_chatwoot(conversation_id, payload)
        except Exception as e:
            print(f"Error sending message to Chatwoot: {e}")