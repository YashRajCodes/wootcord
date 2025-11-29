# wootcord

Wootcord connects Chatwoot to Discord so your support team can see conversations and reply to customers directly from a Discord forum. It receives Chatwoot webhooks, creates or updates threads in a configured Discord Forum channel, and relays messages both ways (Chatwoot -> Discord and Discord -> Chatwoot).

## Highlights
- Automatically creates a Discord thread (in a Forum channel) for new Chatwoot conversations.
- Sends incoming Chatwoot messages into the associated Discord thread.
- Forwards Discord thread replies back into Chatwoot (so agents can reply from Discord).
- Uses Redis + Celery to queue and process webhook events reliably.

## Quick overview
- `webhook/` runs a small Flask app that listens for Chatwoot webhooks and queues them.
- `wootcord/` runs a Discord bot that processes queued events and manages Discord threads.

## Prerequisites
- Python 3.10+ (recommended)
- A Chatwoot instance
- A running Redis instance (used as Celery broker)
- A Discord bot token and a Discord Forum channel where the bot can create threads

## Required environment variables
Create a `.env` file in the project root (or export these in your environment). Example:

    DISCORD_BOT_TOKEN=your_discord_bot_token_here
    FORUM_CHANNEL_ID=123456789012345678
    REDIS_PASSWORD=strong_redis_password
    CHATWOOT_BASE_URL=https://chatwoot.example.com
    CHATWOOT_ACCOUNT_ID=1
    CHATWOOT_API_KEY=your_chatwoot_api_key_here
    WEBHOOK_SECRET=some-secret-for-chatwoot-webhook

Notes:
- `FORUM_CHANNEL_ID` must be a ForumChannel where the bot has permission to create threads and webhooks.
- `CHATWOOT_API_KEY` must be a user access token, which can be generated from Profile Settings after logging into your Chatwoot account.

## Installation
1. Clone the repository and change into it.
2. Create a Python virtual environment and install dependencies:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Create a `.env` using the variables above (or rename `.env.example` to `.env` and replace the values)

## Running locally
There are two services to run:

- The webhook receiver (Flask app): listens on port 3535 for Chatwoot webhooks at `/webhook/<WEBHOOK_SECRET>`.
- The Discord bot (runs the bot and starts a background Celery worker in a thread).

You can start everything using the included helper script which also starts Redis via Docker Compose:

	./start.sh

## Configuring Chatwoot webhook
In your Chatwoot account create a webhook that points to:

	https://<host>:3535/webhook/<WEBHOOK_SECRET>

Select the events you want to send. At minimum the project consumes events like:
- `conversation_created`
- `message_created`
- `conversation_updated`
- `conversation_status_changed`
- typing events (optional)

The webhook receiver simply enqueues the raw payload and the worker will route the event types to the correct handler.

## Contributing
Contributions are welcome! Feel free to fork the repo and submit a pull request or open an issue for reporting bugs and feature requests.