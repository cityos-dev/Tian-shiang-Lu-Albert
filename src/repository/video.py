import uuid

from pymongo import MongoClient

from entities import Video
from .errors import VideoExistsError, VideoNotFoundError


class VideoRepository:

    def __init__(self, client: MongoClient):
        self.videos = client.db.videos

    def create_video(self, content: bin):
        name = str(uuid.uuid4())
        result = self.videos.insert_one({'name': name, 'content': content})
        if result.inserted_count == 0:
            # since video name is uuid, this is an unexpected error
            raise VideoExistsError(name=name)
        return Video(name=name, content=content)

    def list_videos(self):
        videos = self.videos.find()
        return [Video(name=video['name'], content=video['content']) for video in videos]

    def delete_video(self, name):
        result = self.videos.delete_one({'name': name})
        if result.deleted_count == 0:
            raise VideoNotFoundError(name=name)

    def get_video(self, name):
        video = self.videos.find_one({'name': name})
        if video is None:
            raise VideoNotFoundError(name=name)
        return Video(name=video['name'], content=video['content'])
