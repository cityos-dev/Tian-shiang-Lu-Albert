import sys
import os
from typing import List

import pytest
from pymongo import MongoClient
from pymongo.results import BulkWriteResult

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities import Video
from repository import VideoRepository
from repository.errors import VideoNotFoundError, VideoExistsError


class MockDBResult():
    def __init__(self, inserted_count: int = 0, deleted_count: int = 0):
        self.inserted_count = inserted_count
        self.deleted_count = deleted_count


@pytest.fixture
def mock_client(mocker):
    client = mocker.MagicMock()
    return client


def test_create_video(mock_client, mocker):
    repo = VideoRepository(mock_client)
    mocker.spy(repo, 'create_video')
    content = b'content'
    mock_client.db.videos.insert_one.return_value = MockDBResult(inserted_count=1)

    video = repo.create_video(content)

    mock_client.db.videos.insert_one.assert_called_once_with({'name': video.name, 'content': content})
    assert isinstance(video, Video)
    assert video.content == content

    # file exists
    mock_client.db.videos.insert_one.return_value = MockDBResult(inserted_count=0)

    with pytest.raises(Exception) as errinfo:
        video = repo.create_video(content)
    assert errinfo.errisinstance(VideoExistsError)
    assert mock_client.db.videos.insert_one.call_count == 2


def test_list_videos(mock_client, mocker):
    repo = VideoRepository(mock_client)
    expected_videos = [
        {'name': 'video1', 'content': b'video1_content'},
        {'name': 'video2', 'content': b'video2_content'}
    ]
    mock_client.db.videos.find = mocker.Mock(return_value=expected_videos)

    videos = repo.list_videos()

    mock_client.db.videos.find.assert_called_once()
    assert isinstance(videos, List)
    assert len(videos) == len(expected_videos)

    for i in range(len(videos)):
        assert videos[i].name == expected_videos[i]['name']
        assert videos[i].content == expected_videos[i]['content']


def test_delete_video(mock_client, mocker):
    repo = VideoRepository(mock_client)
    mock_client.db.videos.delete_one.return_value = MockDBResult(deleted_count=1)

    repo.delete_video('video1')

    mock_client.db.videos.delete_one.assert_called_once_with({'name': 'video1'})

    # file not found
    mock_client.db.videos.delete_one.return_value = MockDBResult(deleted_count=0)

    with pytest.raises(Exception) as errinfo:
        video = repo.delete_video('video2')
    assert errinfo.errisinstance(VideoNotFoundError)
    assert mock_client.db.videos.delete_one.call_count == 2


def test_get_video(mock_client, mocker):
    repo = VideoRepository(mock_client)
    expected_video = {'name': 'video1', 'content': b'video1_content'}
    mock_client.db.videos.find_one = mocker.Mock(return_value=expected_video)

    video = repo.get_video('video1')

    mock_client.db.videos.find_one.assert_called_once_with({'name': 'video1'})
    assert video.name == expected_video['name']
    assert video.content == expected_video['content']

    # file not found
    mock_client.db.videos.find_one.return_value = None

    with pytest.raises(Exception) as errinfo:
        video = repo.get_video('video2')
    assert errinfo.errisinstance(VideoNotFoundError)
    assert mock_client.db.videos.find_one.call_count == 2
