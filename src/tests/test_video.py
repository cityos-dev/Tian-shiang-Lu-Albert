import sys
import os
from datetime import datetime
from typing import List

import pytest
from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import BulkWriteResult

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities import Video
from entities.video import VideoType
from repositories import VideoRepository
from repositories.errors import VideoNotFoundError, VideoExistsError


class MockDBResult():
    def __init__(self, inserted_count: int = 0, deleted_count: int = 0,
                 inserted_id: str = ''):
        self.inserted_id = inserted_id
        self.inserted_count = inserted_count
        self.deleted_count = deleted_count


@pytest.fixture
def mock_client(mocker):
    client = mocker.MagicMock()
    return client


def test_create_video(mock_client, mocker):
    repo = VideoRepository(mock_client)
    mocker.spy(repo, 'create_video')
    name = 'video'
    content = b'content'
    video_type = VideoType.MP4

    video = repo.create_video(name=name, content=content, video_type=video_type)

    mock_client.db.videos.insert_one.assert_called_once()
    assert isinstance(video, Video)
    assert video.content == content
    assert video.name == name
    assert video.video_type == video_type


def test_list_videos(mock_client, mocker):
    repo = VideoRepository(mock_client)
    video1_created_at = datetime.utcnow()
    video2_created_at = datetime.utcnow()
    expected_videos = [
        {'_id': ObjectId('63f0c5b14f447e928ba3e6af'), 'name': 'video1', 'size': 7, 'content': b'1111111', 'video_type': VideoType.MPG.name, 'created_at': video1_created_at},
        {'_id': ObjectId('63f0c5bb4f447e928ba3e6b0'), 'name': 'video2', 'size': 3, 'content': b'123', 'video_type': VideoType.MP4.name, 'created_at': video2_created_at}
    ]
    mock_client.db.videos.find = mocker.Mock(return_value=expected_videos)

    videos = repo.list_videos()

    mock_client.db.videos.find.assert_called_once()
    assert isinstance(videos, List)
    assert len(videos) == len(expected_videos)

    for i in range(len(videos)):
        assert videos[i].file_id == str(expected_videos[i]['_id'])
        assert videos[i].name == expected_videos[i]['name']
        assert videos[i].size == expected_videos[i]['size']
        assert videos[i].video_type.name == expected_videos[i]['video_type']
        assert videos[i].created_at == expected_videos[i]['created_at']


def test_delete_video(mock_client, mocker):
    repo = VideoRepository(mock_client)
    mock_client.db.videos.delete_one.return_value = MockDBResult(deleted_count=1)

    repo.delete_video('63f0c5b14f447e928ba3e6af')

    mock_client.db.videos.delete_one.assert_called_once_with({'_id': ObjectId('63f0c5b14f447e928ba3e6af')})

    # file not found
    mock_client.db.videos.delete_one.return_value = MockDBResult(deleted_count=0)

    with pytest.raises(Exception) as errinfo:
        video = repo.delete_video('63f0c5bb4f447e928ba3e6b0')
    assert errinfo.errisinstance(VideoNotFoundError)
    assert mock_client.db.videos.delete_one.call_count == 2


def test_get_video(mock_client, mocker):
    repo = VideoRepository(mock_client)
    created_at = datetime.utcnow()
    expected_video = {'_id': ObjectId('63f0c5b14f447e928ba3e6af'), 'name': 'video1', 'size': 7, 'content': b'1111111',
                      'video_type': VideoType.MP4.name, 'created_at': created_at}
    mock_client.db.videos.find_one = mocker.Mock(return_value=expected_video)

    video = repo.get_video('63f0c5b14f447e928ba3e6af')

    mock_client.db.videos.find_one.assert_called_once_with({'_id': ObjectId('63f0c5b14f447e928ba3e6af')})
    assert video.file_id == str(expected_video['_id'])
    assert video.name == expected_video['name']
    assert video.content == expected_video['content']
    assert video.video_type.name == expected_video['video_type']
    assert video.size == expected_video['size']
    assert video.created_at == created_at

    # file not found
    mock_client.db.videos.find_one.return_value = None

    with pytest.raises(Exception) as errinfo:
        video = repo.get_video('63f0c5bb4f447e928ba3eaaa')
    assert errinfo.errisinstance(VideoNotFoundError)
    assert mock_client.db.videos.find_one.call_count == 2
