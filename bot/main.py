import asyncio

import config
import discord

from discord.ext import commands
from handlers import dispatcher 
from tasks import queue
from typing import override

@queue.task(name=config.task_name, bind=True)
def queue_handler(self, data):
    try:
        loop = bot_instance.loop
        asyncio.run_coroutine_threadsafe(dispatcher.dispatch(data), loop).result()
    except Exception as e:
        print(f"({self.request.retries}/{self.max_retries}) An error occured while passing data to bot: {e}")
        raise self.retry(exc=e, countdown=2**self.request.retries, max_retries=3)

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(
               command_prefix=self.determine_prefix,
               status=discord.Status.online,
               activity=discord.Activity(type=discord.ActivityType.playing, name="chatwoot"),
               intents=discord.Intents.all()
		)
          
	async def determine_prefix(self, bot: commands.Bot, message: discord.Message):
		return '>' # make a config for it if needed
     
	async def on_ready(self):
		print(f'Bot is ready. Logged in as {self.user.name}')

	def run_celery_worker(self):
		print("Celery worker thread is starting...")
		argv = [
			'worker',
			'-P', 'threads',
			#'--loglevel=info'
		]
		queue.worker_main(argv)
    
	@override
	async def start(self):
		loop = asyncio.get_running_loop()
		celery_worker = loop.run_in_executor(None, self.run_celery_worker)

		async with self:
			print("Starting the bot...")
			await super().start(config.bot_token)

		await celery_worker

if __name__ == '__main__':
	bot_instance = Bot()
	asyncio.run(bot_instance.start())
