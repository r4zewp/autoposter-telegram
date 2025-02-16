from supabase import create_client, Client
from config.core import core
from aiogram import BaseMiddleware

supabase_client: Client = create_client(core.SUPABASE_URL, core.SUPABASE_KEY)

class SupabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data["supabase_client"] = supabase_client
        return await handler(event, data)
