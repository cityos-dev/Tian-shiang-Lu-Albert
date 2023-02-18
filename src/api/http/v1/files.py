from flask import Blueprint
from http import HTTPStatus

from repository import video_repository as video_repo
from repository.errors import VideoExistsError, VideoNotFoundError

routes = Blueprint('file', __name__)


@routes.get('/v1/files/<fileid>')
def get_file(fileid):
    try:
        return video_repo.get(fileid)
    except VideoNotFoundError as e:
        return "", HTTPStatus.NOT_FOUND


@routes.delete('/v1/files/<fileid>')
def delete_file(fileid):
    return video_repo.delete(fileid)


@routes.post('/v1/files')
def upload_file():
    return video_repo.create(request.data)


@routes.get('/v1/files')
def list_files():
    return video_repo.list()
