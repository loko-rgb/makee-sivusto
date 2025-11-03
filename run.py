from app import create_app, socketio


def create():
    app = create_app()
    return app
def run(app):
    socketio.run(app)

run(create())