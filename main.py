import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.core import core
from middlewares import supabase_middleware as sm
from handlers.youtube_handlers import register_handlers
from scheduler.youtube_scheduler import start_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main() -> None:
    """Initialize and start the bot"""
    # Initialize bot and dispatcher
    bot = Bot(token=core.TOKEN)
    dp = Dispatcher()

    try:
        # Register message handlers
        register_handlers(dp)
        
        # Setup middleware
        dp.message.middleware(sm.SupabaseMiddleware())
        
        # Start scheduler in background
        start_scheduler(bot, sm.supabase_client)
        
        # Start polling
        logger.info("Starting bot...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f'An error occurred: {e}')
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
