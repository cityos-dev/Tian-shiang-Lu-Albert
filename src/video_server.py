from flask import Flask
from pymongo import MongoClient
from waitress import serve

from api.http.v1 import health, files

app = Flask(__name__)


def create_video_server():
    app = Flask(__name__)
    app.register_blueprint(health.routes)
    app.register_blueprint(files.routes)
    return app


if __name__ == '__main__':
    app = create_video_server()
    serve(app, host='0.0.0.0', port=8080)
