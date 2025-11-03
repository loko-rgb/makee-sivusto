from app import create_app, socketio


def create():
    app = create_app()
    return app

def run():
    app = create()
    socketio.run(app)

if __name__ == "__main__":
    run()