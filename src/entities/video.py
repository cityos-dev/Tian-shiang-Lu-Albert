from datetime import datetime
from enum import Enum


class VideoType(Enum):
    MP4 = 'mp4'
    MPG = 'mpg'

    @classmethod
    def from_name(cls, name: str):
        extension = name.split('.')[-1]
        try:
            return cls[extension.upper()]
        except KeyError:
            return None


class Video():
    def __init__(self, file_id: str, name: str, content: bin, size: int,
                 video_type: VideoType, created_at: datetime):
        self.file_id = file_id
        self.name = name
        self.content = content
        self.video_type = video_type
        self.size = size
        self.created_at = created_at
