import discord
from discord.ext import commands

from pydantic import ConfigDict, validate_call
from wootcord.models import ConversationCreated
from wootcord.utils.redis import store_mappings

@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
async def handle(bot: commands.Bot, data: ConversationCreated):
    info = discord.Embed(
        title="Conversation Info",
        color=discord.Color.blue()
    )

    info.add_field(name="Conversation ID:", value=str(data.id), inline=False)
    info.add_field(name="Created By:", value=f"{data.meta.sender.id} - {data.meta.sender.name}", inline=False)
    info.add_field(name="Status:", value=data.status, inline=False)
    
    thread, initial_message = await bot.forum.create_thread(
        name = f"#{data.id} - {data.meta.sender.name}",
        embed=info
    )

    await store_mappings(data.id, thread.id)

    webhook = (await bot.forum.webhooks() or [None])[0] or await bot.forum.create_webhook(name="Wootcord")

    for message in data.messages:
        await webhook.send(content=message.content, username=data.meta.sender.name, allowed_mentions=discord.AllowedMentions.none(), thread=thread)
    
