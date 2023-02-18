from datetime import datetime

from pymongo import MongoClient
from bson import ObjectId

from entities import Video
from entities.video import VideoType
from .errors import VideoExistsError, VideoNotFoundError


class VideoRepository:

    def __init__(self, client: MongoClient):
        self.videos = client.db.videos

    def create_video(self, name: str, content: bin, video_type: VideoType):
        created_at = datetime.utcnow()
        size = len(content)
        result = self.videos.insert_one({'name': name, 'content': content, 'video_type': video_type.name,
                                         'size': size, 'created_at': created_at})
        return Video(file_id=str(result.inserted_id), name=name, content=content,
                     size=size, video_type=video_type, created_at=created_at)

    def list_videos(self):
        videos = self.videos.find()
        return [Video(file_id=str(video['_id']), name=video['name'], size=video['size'],
                      content=video['content'], video_type=VideoType.from_name(video['video_type']),
                      created_at=video['created_at']) for video in videos]

    def delete_video(self, file_id: str):
        result = self.videos.delete_one({'_id': ObjectId(file_id)})
        if result.deleted_count == 0:
            raise VideoNotFoundError(file_id=file_id)

    def get_video(self, file_id: str) -> Video:
        video = self.videos.find_one({'_id': ObjectId(file_id)})
        if video is None:
            raise VideoNotFoundError(file_id=file_id)
        return Video(file_id=str(video['_id']), name=video['name'], size=video['size'],
                     content=video['content'], video_type=VideoType.from_name(video['video_type']),
                     created_at=video['created_at'])
