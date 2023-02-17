from pymongo import MongoClient

import setting
from .video import VideoRepository


mongo_client = MongoClient(setting.mongo_uri)
video_repository = VideoRepository(mongo_client)

__all__ = [video_repository, VideoRepository]
