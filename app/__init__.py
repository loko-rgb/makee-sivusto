import flask
from datetime import timedelta
import os
import threading
from .events import socketio
from flask_session import Session
from .routes import main
import time
from cachelib.file import FileSystemCache


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(main)
    app.config.update({"DEBUG" : True,
        "SESSION_PERMANENT" : True,
        "PERMANENT_SESSION_LIFETIME" : timedelta(seconds=5),
        "SECRET_KEY" : "kjdvlsdk jo0439w jI)OY/)8TY(/gf hq87w0Å'ÅW'EÅRG WJUE9RHG9HE9RHG 379WY0P jqwq9f0pfhQF8G78Q03 G8 hi ag ayigsai8äwer'tprhuå6ä780rjkkä'r6k708ipodrijwhs)",
        "SESSION_TYPE" : "cachelib",
        "SESSION_SERIALIZATION_FORMAT" : 'json',
        "SESSION_CACHELIB" : FileSystemCache(threshold=500, cache_dir= 'session'),
        "SESSION_CLEANUP_N_REQUEST" : 3
        })
    Session(app)

    socketio.init_app(app, cors_allowed_origins="*")

    return app