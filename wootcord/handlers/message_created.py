import discord
from discord.ext import commands

from pydantic import ConfigDict, validate_call
from wootcord.models import MessageCreated
from wootcord.utils.redis import get_thread_id

@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
async def handle(bot: commands.Bot, data: MessageCreated):
    thread_id = await get_thread_id(data.conversation.id)
    if not thread_id:
        print(f"No thread mapping found for conversation id: {data.conversation.id}. Skipping.")
        return

    thread = await bot.fetch_channel(thread_id)
    webhook = (await bot.forum.webhooks() or [None])[0] or await bot.forum.create_webhook(name="Wootcord")

    avatar_url = None
    if data.conversation and data.conversation.messages:
        latest = data.conversation.messages[0]
        avatar_url = getattr(latest.sender, "avatar_url", None)

    await webhook.send(content=data.content, username=data.sender.name, avatar_url=avatar_url, allowed_mentions=discord.AllowedMentions.none(), thread=thread)