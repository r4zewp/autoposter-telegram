from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from supabase import Client

from config.core import core

import asyncio
import logging

from services import youtube_service as ys
from services import generate_message as gm
from middlewares import supabase_middleware as sm

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=core.TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Hello! I am YouLookSmart Bot. I can send you updates about new videos on my channel.')

@dp.message(Command('check'))
async def youtube_command(message: Message, supabase_client: Client):
    await message.answer('YouTube updates will be sent to you soon!')
    new_videos = await ys.check_youtube(supabase_client)
    for video in new_videos:
        await bot.send_message(
            chat_id='@youlooksmart', 
            text=gm.generate_message(video.link, video.title, video.summary),
            parse_mode="HTML"
            )


async def main():
    logging.info('Starting bot polling...')
    try:
        logging.info('Attempting to start bot polling...')
        dp.message.middleware(sm.SupabaseMiddleware())
        await dp.start_polling(bot)
        logging.info('Bot polling started successfully.')
    except Exception as e:
        logging.error(f'An error occurred: {e}')
    finally:
        logging.info('Closing bot session...')
        await bot.session.close()
        logging.info('Bot session closed successfully.')

if __name__ == "__main__":
    asyncio.run(main())
