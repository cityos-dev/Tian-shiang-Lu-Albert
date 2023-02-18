from flask import Blueprint

routes = Blueprint('health', __name__)


@routes.get('/v1/health')
def health_check():
    return ''
