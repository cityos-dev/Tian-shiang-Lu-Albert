from flask import Blueprint

routes = Blueprint('v1_health', __name__, url_prefix='/v1/health')


@routes.get('')
def health_check():
    return ''
