from datetime import datetime


class Video():
    def __init__(self, file_id: str, name: str, content: bin, size: int,
                 content_type: str, created_at: datetime):
        self.file_id = file_id
        self.name = name
        self.content = content
        self.content_type = content_type
        self.size = size
        self.created_at = created_at
