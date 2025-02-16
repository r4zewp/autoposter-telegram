import asyncio
import schedule
import time
import threading
import logging
from aiogram import Bot
from supabase import Client

from handlers.youtube_handlers import check_and_post_youtube_updates

logger = logging.getLogger(__name__)

def run_youtube_checker(bot: Bot, supabase_client: Client) -> None:
    """Run the YouTube checker in the scheduler"""
    asyncio.run(check_and_post_youtube_updates(bot, supabase_client))

def start_scheduler(bot: Bot, supabase_client: Client) -> threading.Thread:
    """Start the scheduler in a separate thread"""
    def run_schedule():
        schedule.every(1).hour.do(lambda: run_youtube_checker(bot, supabase_client))
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    schedule_thread = threading.Thread(target=run_schedule, daemon=True)
    schedule_thread.start()
    logger.info("YouTube check scheduler started")
    return schedule_thread
