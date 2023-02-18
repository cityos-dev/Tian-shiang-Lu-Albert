from flask import Blueprint, request, make_response
from http import HTTPStatus

from entities.video import VideoType
from repository import video_repository as video_repo
from repository.errors import VideoExistsError, VideoNotFoundError

routes = Blueprint('v1_files', __name__, url_prefix='/v1')


@routes.get('/files/<fileid>')
def get_file(fileid):
    print('list file')
    try:
        video = video_repo.get_video(fileid)
        return video.content
    except VideoNotFoundError as err:
        return '', HTTPStatus.NOT_FOUND


@routes.delete('/files/<fileid>')
def delete_file(fileid):
    try:
        video_repo.delete_video(fileid)
        return '', HTTPStatus.NO_CONTENT
    except VideoNotFoundError as err:
        return '', HTTPStatus.NOT_FOUND


@routes.post('/files')
def upload_file():
    if 'Content-Type' not in request.headers:
        return '', HTTPStatus.BAD_REQUEST
    file = request.files['data']
    video = video_repo.create_video(name=file.filename, content=file.read(), video_type=video_type)
    response = make_response('', HTTPStatus.CREATED)
    # TODO this code must be orginized with a conbination of real domain and port
    location = 'http://0.0.0.0:8080/v1/files/{}'.format(video.file_id)
    response.headers = {'Location': location}
    return response


@routes.get('/files')
def list_files():
    print('list file')
    videos = video_repo.list_videos()
    return [{'fileid': video.file_id, 'name': video.name,
             'size': video.size, 'created_at': video.created_at}
            for video in videos]
