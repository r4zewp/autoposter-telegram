from dotenv import load_dotenv
import os

load_dotenv()

class Core:
    """Core configuration class that handles both local and Cloudflare environments"""
    
    def __init__(self):
        # Try to load from .env file for local development
        load_dotenv()
        
        # Initialize with None to handle both environments
        self._token: Optional[str] = None
        self._youtube: Optional[str] = None
        self._supabase_url: Optional[str] = None
        self._supabase_key: Optional[str] = None
        self._telegram_channel: Optional[str] = None
        self._environment: Optional[str] = None
        
        # Load configuration
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from environment variables"""
        # Token (support both TOKEN and TELEGRAM_BOT_TOKEN for compatibility)
        self._token = os.getenv('TOKEN') or os.getenv('TELEGRAM_BOT_TOKEN')
        if not self._token:
            raise ValueError("Telegram bot token not found in environment variables")
        
        # YouTube RSS feed URL
        self._youtube = os.getenv('YOUTUBE')
        if not self._youtube:
            raise ValueError("YouTube RSS feed URL not found in environment variables")
        
        # Supabase configuration
        self._supabase_url = os.getenv('SUPABASE_URL')
        self._supabase_key = os.getenv('SUPABASE_KEY')
        if not self._supabase_url or not self._supabase_key:
            raise ValueError("Supabase configuration not found in environment variables")
        
        # Telegram channel
        self._telegram_channel = os.getenv('TELEGRAM_CHANNEL')
        if not self._telegram_channel:
            raise ValueError("Telegram channel not found in environment variables")
        
        # Environment (development/production)
        self._environment = os.getenv('ENVIRONMENT', 'development')
    
    @property
    def TOKEN(self) -> str:
        return self._token
    
    @property
    def YOUTUBE(self) -> str:
        return self._youtube
    
    @property
    def SUPABASE_URL(self) -> str:
        return self._supabase_url
    
    @property
    def SUPABASE_KEY(self) -> str:
        return self._supabase_key
    
    @property
    def TELEGRAM_CHANNEL(self) -> str:
        return self._telegram_channel
    
    @property
    def ENVIRONMENT(self) -> str:
        return self._environment
    
    @property
    def IS_DEVELOPMENT(self) -> bool:
        return self._environment.lower() == 'development'
    
    @property
    def IS_PRODUCTION(self) -> bool:
        return self._environment.lower() == 'production'

# Create a singleton instance
core = Core()