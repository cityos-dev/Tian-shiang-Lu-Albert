from .base import RepositoryError


class VideoNotFoundError(RepositoryError):

    def __init__(self, file_id: str):
        super(VideoNotFoundError, self).__init__("Couldn't find video `%s`".format(file_id))
        self._file_id = file_id

    def get_video_id(self) -> str:
        return self._file_id


class VideoExistsError(RepositoryError):

    def __init__(self, name: str):
        super(VideoExistsError, self).__init__('Video `%s` already exists'.format(name))
        self._name = name

    def get_video_name(self) -> str:
        return self._name
