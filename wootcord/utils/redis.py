import redis.asyncio as redis
from .. import config

redis_pool = redis.from_url(config.broker_url)

async def store_mappings(conversation_id: int, thread_id: int):
    cw_key = f"wootcord.cw_conv:{conversation_id}"
    dc_key = f"wootcord.dc_thread:{thread_id}"

    await redis_pool.set(cw_key, thread_id)
    await redis_pool.set(dc_key, conversation_id)

    print(f"Stored mappings in Redis: {cw_key} -> {thread_id}, {dc_key} -> {conversation_id}")

async def delete_mappings(conversation_id: int, thread_id: int):
    cw_key = f"wootcord.cw_conv:{conversation_id}"
    dc_key = f"wootcord.dc_thread:{thread_id}"

    await redis_pool.delete(cw_key)
    await redis_pool.delete(dc_key)

    print(f"Deleted mappings from Redis: {cw_key} and {dc_key}")

async def get_thread_id(conversation_id: int) -> int | None:
    cw_key = f"wootcord.cw_conv:{conversation_id}"
    thread_id = await redis_pool.get(cw_key)
    return int(thread_id) if thread_id else None

async def get_conversation_id(thread_id: int) -> int | None:
    dc_key = f"wootcord.dc_thread:{thread_id}"
    conversation_id = await redis_pool.get(dc_key)
    return int(conversation_id) if conversation_id else None 