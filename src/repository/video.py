from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient

from entities import Video
from entities.video import VideoType
from .errors import VideoExistsError, VideoNotFoundError


class VideoRepository:

    def __init__(self, client: MongoClient):
        self.videos = client.db.videos

    def create_video(self, name: str, content: bin, video_type: VideoType):
        created_at = datetime.utcnow()
        size = len(content)
        video = Video(file_id=ObjectId(), name=name, content=content, size=size,
                      video_type=video_type, created_at=created_at)
        self.videos.insert_one({'_id': video.file_id, 'name': video.name,
                                'content': video.content, 'video_type': video.video_type.name,
                                'size': video.size, 'created_at': video.created_at})
        return video

    def list_videos(self):
        videos = self.videos.find()
        return [Video(file_id=str(video['_id']), name=video['name'], size=video['size'],
                      content=video['content'], video_type=VideoType.from_name(video['video_type']),
                      created_at=video['created_at']) for video in videos]

    def delete_video(self, file_id: str):
        if len(file_id) != 24:
            raise VideoNotFoundError(file_id=file_id)

        result = self.videos.delete_one({'_id': ObjectId(file_id)})
        if result.deleted_count == 0:
            raise VideoNotFoundError(file_id=file_id)

    def get_video(self, file_id: str) -> Video:
        if len(file_id) != 24:
            raise VideoNotFoundError(file_id=file_id)

        video = self.videos.find_one({'_id': ObjectId(file_id)})
        if video is None:
            raise VideoNotFoundError(file_id=file_id)
        return Video(file_id=str(video['_id']), name=video['name'], size=video['size'],
                     content=video['content'], video_type=VideoType.from_name(video['video_type']),
                     created_at=video['created_at'])
