from flask import Blueprint, request
from http import HTTPStatus

from entities.video import VideoType
from repository import video_repository as video_repo
from repository.errors import VideoExistsError, VideoNotFoundError

routes = Blueprint('v1_file', __name__, url_prefix='/v1/files')


@routes.get('/<fileid>')
def get_file(fileid):
    try:
        video = video_repo.get(fileid)
        return video.content
    except VideoNotFoundError as err:
        return '', HTTPStatus.NOT_FOUND


@routes.delete('/<fileid>')
def delete_file(fileid):
    try:
        video_repo.delete(fileid)
        return '', HTTPStatus.NO_CONTENT
    except VideoNotFoundError as err:
        return '', HTTPStatus.NOT_FOUND


@routes.post('')
def upload_file():
    if 'Content-Type' not in request.headers:
        return '', HTTPStatus.BAD_REQUEST
    content_type = request.headers['Content-Type']
    file = request.files['file']
    video_type = get_video_type(content_type)
    if video_type is None:
        return '', HTTPStatus.BAD_REQUEST

    fileid = video_repo.create(name=file.filename, content=file, video_type=video_type)
    return {'Location': fileid}, HTTPStatus.CREATED


def get_video_type(content_type: str):
    if content_type == 'multipart/form-data':
        return VideoType.STREAM
    elif content_type == 'video/mp4':
        return VideoType.MP4
    elif content_type == 'video/mpg':
        return VideoType.MPG


@routes.get('')
def list_files():
    videos = video_repo.list_videos()
    return [{'fileid': video.file_id, 'name': video.name, 'size': video.size, created_at: video.created_at}
            for video in videos]
