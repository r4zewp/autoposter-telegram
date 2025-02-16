class Video:
    
    def __init__(self, youtube_id, title, summary, link):
        
        self.youtube_id = youtube_id
        self.title = title
        self.summary = summary
        self.link = link
    
    def __repr__(self):
        return f"Video(youtube_id={self.youtube_id}, title={self.title}, summary={self.summary}, link={self.link})"   

    def to_dict(self):
        return {
            
            "youtube_id": self.youtube_id,
            "title": self.title,
            "summary": self.summary,
            "link": self.link
        }
    
    def from_dict(self, dict):
        
        self.youtube_id = dict["youtube_id"]
        self.title = dict["title"]
        self.summary = dict["summary"]
        self.link = dict["link"]

    keys = ["youtube_id", "title", "summary"]