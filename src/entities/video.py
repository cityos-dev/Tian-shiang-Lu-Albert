from datetime import datetime
from enum import Enum

from .errors.common import TypeNotSupportedError


class VideoType(Enum):
    MP4 = 'mp4'
    MPG = 'mpg'
    STREAM = 'stream'

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name.upper()]
        except KeyError:
            raise TypeNotSupportedError(name)


class Video():
    def __init__(self, file_id: str, name: str, content: bin, size: int,
                 content_type: VideoType, created_at: datetime):
        self.file_id = file_id
        self.name = name
        self.content = content
        self.content_type = content_type
        self.size = size
        self.created_at = created_at
