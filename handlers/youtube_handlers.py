from aiogram import Bot, types
from aiogram.filters import Command, CommandStart
from supabase import Client
import logging

from services import youtube_service as ys
from services import generate_message as gm
from config.core import core

logger = logging.getLogger(__name__)

async def check_and_post_youtube_updates(bot: Bot, supabase_client: Client) -> None:
    """Check for new YouTube videos and post them to the channel"""
    try:
        new_videos = await ys.check_youtube(supabase_client)
        
        if new_videos:
            for video in new_videos:
                await bot.send_message(
                    chat_id=core.TELEGRAM_CHANNEL, 
                    text=gm.generate_message(video.link, video.title, video.summary),
                    parse_mode="HTML"
                )
            logger.info(f"Posted {len(new_videos)} new videos")
        else:
            logger.info("No new videos found")
    except Exception as e:
        logger.error(f"Error in periodic YouTube check: {e}")

async def handle_start_command(message: types.Message) -> None:
    """Handle /start command"""
    await message.answer('Hello! I am YouLookSmart Bot. I can send you updates about new videos on my channel.')

async def handle_check_command(message: types.Message, bot: Bot, supabase_client: Client) -> None:
    """Handle /check command - manually check for new videos"""
    try:
        await message.answer("Checking for new YouTube videos...")
        await check_and_post_youtube_updates(bot, supabase_client)
        await message.answer("Check completed!")
    except Exception as e:
        logger.error(f"Error in manual YouTube check: {e}")
        await message.answer(f"An error occurred: {e}")

def register_handlers(dp) -> None:
    """Register all handlers"""
    dp.message.register(handle_start_command, CommandStart())
    dp.message.register(handle_check_command, Command("check"))
