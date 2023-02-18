from flask import Blueprint

routes = Blueprint('health', __name__)


@routes.get('/health')
def health_check():
    return ''
