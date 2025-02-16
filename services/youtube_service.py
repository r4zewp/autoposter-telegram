import feedparser
from dataclasses import dataclass
import logging
from typing import List

from supabase import Client
from config.core import core

logger = logging.getLogger(__name__)

@dataclass
class Video:
    youtube_id: str
    title: str
    summary: str
    link: str

def remove_hashtags(title: str, summary: str) -> tuple[str, str]:
    """Remove hashtags from title and summary"""
    title = ' '.join(word for word in title.split() if not word.startswith('#'))
    summary = ' '.join(word for word in summary.split() if not word.startswith('#'))
    return title, summary

async def check_youtube(supabase_client: Client) -> List[Video]:
    """Check YouTube RSS feed for new videos"""
    try:
        feed = feedparser.parse(core.YOUTUBE)
        
        print(feed.entries)

        # Get existing videos from database
        supabase_videos = supabase_client.table('videos').select("*").execute()
        existing_videos = supabase_videos.data
        
        # Create set of existing video IDs for quick lookup
        existing_ids = {video["youtube_id"] for video in existing_videos}
        
        # Process new videos
        new_videos: List[Video] = []
        for_supabase: List[dict] = []
        
        for video in feed.entries:
            if video.id not in existing_ids:
                title, summary = remove_hashtags(title=video.title, summary=video.summary)
                new_videos.append(
                    Video(
                        youtube_id=video.id,
                        title=title,
                        summary=summary,
                        link=video.link
                    )
                )
                for_supabase.append({
                    "youtube_id": video.id,
                    "title": title,
                    "summary": summary
                })
        
        # Add new videos to database
        if for_supabase:
            supabase_client.table('videos').insert(for_supabase).execute()
            logger.info(f"Added {len(for_supabase)} new videos to database")
        
        return new_videos
        
    except Exception as e:
        logger.error(f"Error checking YouTube feed: {e}")
        return []