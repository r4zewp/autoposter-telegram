import feedparser

from models.video import Video

from config.core import core
from services.remove_hashtags import remove_hashtags

async def check_youtube(supabase_client):
    feed = feedparser.parse(core.YOUTUBE)
    
    feed_videos = []
    for_supabase = []

    if feed.entries:
        # Получаем видео из Supabase
        supabase_videos = supabase_client.table('videos').select("*").execute()
        existing_videos = supabase_videos.data  # список словарей, где есть ключ "youtube_id"

        # Создаем множество существующих youtube_id для быстрой проверки
        existing_ids = {video["youtube_id"] for video in existing_videos}
        

        # Фильтруем только новые видео, которых еще нет в базе
        feed_videos: list[Video] = []
        for video in feed.entries:
            if video.id not in existing_ids:
                title, summary = remove_hashtags(title=video.title, summary=video.summary)
                feed_videos.append(Video(youtube_id=video.id, title=title, summary=summary, link=video.link))
                for_supabase.append({"youtube_id": video.id, "title": title, "summary": summary})
        
        # Добавляем новые видео в базу
        supabase_client.table('videos').insert(for_supabase).execute()
        
        return feed_videos

        # entry = feed.entries[0]
        
        # link = entry.link 
        # return title, summary, link
        
    return None, None

# last_video = None

# while True:
#     title, link = check_youtube()
#     if title and link and link != last_video:
#         message = f"Новое видео: {title}\nСмотреть: {link}"
#         post_to_telegram(message)
#         last_video = link
#         print("Опубликовано новое видео:", title)
#     time.sleep(300)  # проверка каждые 5 минут