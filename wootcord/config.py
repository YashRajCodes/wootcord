import os
import dotenv

dotenv.load_dotenv()

bot_token = os.getenv("DISCORD_BOT_TOKEN")
forum_channel_id = int(os.getenv("FORUM_CHANNEL_ID", "0"))

task_name = "wootcord.process_webhooks"
redis_password = os.getenv('REDIS_PASSWORD')
broker_url = f'redis://:{redis_password}@localhost:6379/0'

chatwoot_base_url = os.getenv("CHATWOOT_BASE_URL")
chatwoot_account_id = int(os.getenv("CHATWOOT_ACCOUNT_ID", "1"))
chatwoot_api_key = os.getenv("CHATWOOT_API_KEY")

if not redis_password:
    raise ValueError("REDIS_PASSWORD environment variable is not set.")
if not chatwoot_base_url:
    raise ValueError("CHATWOOT_BASE_URL environment variable is not set.")
if not chatwoot_api_key:
    raise ValueError("CHATWOOT_API_KEY environment variable is not set.")