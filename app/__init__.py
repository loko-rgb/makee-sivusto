import flask
from datetime import timedelta
import os
import threading
from .events import socketio
from flask_session import Session
from .routes import main
import time
from cachelib.file import FileSystemCache
import struct
import pickle
import os

def chcecker():
    while True:
        minutes = 10
        for filename in os.listdir("session"):
            with open("session/" + filename, 'rb') as f:
                data = f.read()
            if len(data) < 17:
                os.remove("session/" + filename)
                continue
            length_bytes = data[9:17]
            payload_length = struct.unpack('>Q', length_bytes)[0]
            payload_bytes = data[16:16+payload_length]
            data11 = b'\x80\x05\x95\x1f\x00\x00\x00\x00\x00\x00\x00}\x94' + payload_bytes
            session_dict = pickle.loads(data11)
            if time.time() > session_dict["last_use"]+30:#60*minutes:
                os.remove("session/" + filename)
        print("CHECKED")
        time.sleep(10)
            


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(main)
    app.config.update({"DEBUG" : True,
        "SESSION_PERMANENT" : True,
        "PERMANENT_SESSION_LIFETIME" : timedelta(minutes=20),
        "SECRET_KEY" : "kjdvlsdk jo0439w jI)OY/)8TY(/gf hq87w0Å'ÅW'EÅRG WJUE9RHG9HE9RHG 379WY0P jqwq9f0pfhQF8G78Q03 G8 hi ag ayigsai8äwer'tprhuå6ä780rjkkä'r6k708ipodrijwhs)",
        "SESSION_TYPE" : "cachelib",
        "SESSION_SERIALIZATION_FORMAT" : 'json',
        "SESSION_CACHELIB" : FileSystemCache(threshold=500, cache_dir= 'session'),
        "SESSION_CLEANUP_N_REQUEST" : 3
        })
    Session(app)

    """if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        if not any(th.name == "chchecker" for th in threading.enumerate()):
            threading.Thread(target=chcecker, daemon=True, name="chchecker").start()"""

    socketio.init_app(app, cors_allowed_origins="*")

    return app