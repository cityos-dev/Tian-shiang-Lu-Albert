from flask import Blueprint, request, make_response
from http import HTTPStatus

from setting import server
from entities.video import VideoType, Video
from repositories import video_repository as video_repo
from repositories.errors import VideoExistsError, VideoNotFoundError

routes = Blueprint('v1_files', __name__, url_prefix='/v1')


@routes.get('/files/<fileid>')
def get_file(fileid):
    print('list file')
    try:
        video = video_repo.get_video(fileid)
        response = make_response(video.content)
        content_type = get_content_type(video)
        if content_type is None:
            return '', HTTPStatus.INTERNAL_SERVER_ERROR

        response.headers = {
            'Content-Type': get_content_type(video),
            'Content-Disposition': 'attachment; filename="{}"'.format(video.name)
        }
        return response
    except VideoNotFoundError as err:
        return '', HTTPStatus.NOT_FOUND


def get_content_type(video: Video):
    video_type = video.video_type
    if video_type == VideoType.MP4:
        return 'video/mp4'
    elif video_type == VideoType.MPG:
        return 'video/mpeg'
    return None


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

    if 'data' not in request.files:
        return '', HTTPStatus.BAD_REQUEST

    file = request.files['data']
    content = file.read()
    if len(content) == 0:
        return '', HTTPStatus.BAD_REQUEST

    name = file.filename
    video_type = VideoType.from_name(name)
    if video_type is None:
        return '', HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    video = video_repo.create_video(name=name, content=content, video_type=video_type)
    response = make_response('', HTTPStatus.CREATED)
    location = 'http://{0}:{1}/v1/files/{2}'.format(server['domain'],
                                                    server['port'],
                                                    video.file_id)
    response.headers = {'Location': location}
    return response


@routes.get('/files')
def list_files():
    print('list file')
    videos = video_repo.list_videos()
    return [{'fileid': video.file_id, 'name': video.name,
             'size': video.size, 'created_at': video.created_at}
            for video in videos]
