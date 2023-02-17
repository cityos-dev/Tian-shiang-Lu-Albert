from .base import RepositoryError


class VideoNotFoundError(RepositoryError):

    def __init__(self, name: str):
        super("Couldn't find video `%s`".format(name))
        self._name = name

    def get_video_name(self) -> str:
        return self._name


class VideoExistsError(RepositoryError):

    def __init__(self, name: str):
        super('Video `%s` already exists'.format(name))
        self._name = name

    def get_video_name(self) -> str:
        return self._name
