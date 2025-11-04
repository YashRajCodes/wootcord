import os
import dotenv

dotenv.load_dotenv()

bot_token = os.getenv("DISCORD_BOT_TOKEN")
forum_channel_id = int(os.getenv("FORUM_CHANNEL_ID", "0"))

task_name = "wootcord.process_webhooks"
redis_password = os.getenv('REDIS_PASSWORD')
broker_url = f'redis://:{redis_password}@localhost:6379/0'

if not redis_password:
    raise ValueError("REDIS_PASSWORD environment variable is not set.")