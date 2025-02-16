from dotenv import load_dotenv
import os

load_dotenv()

class Core:

    def __init__(self):
        self.TOKEN=os.getenv("TOKEN")
        self.YOUTUBE=os.getenv("YOUTUBE")
        self.SUPABASE_URL=os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY=os.getenv("SUPABASE_KEY")
        self.TELEGRAM_CHANNEL=os.getenv("TELEGRAM_CHANNEL")

core = Core()