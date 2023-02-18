from datetime import datetime
from enum import Enum


class VideoType(Enum):
    MP4 = 'mp4'
    MPG = 'mpg'
    STREAM = 'stream'

    @classmethod
    def from_name(cls, name: str):
        return cls[name.upper()]


class Video():
    def __init__(self, file_id: str, name: str, content: bin, size: int,
                 video_type: VideoType, created_at: datetime):
        self.file_id = file_id
        self.name = name
        self.content = content
        self.video_type = video_type
        self.size = size
        self.created_at = created_at
