from app import create_app, socketio

create = create_app()

def run(app):
    socketio.run(app)

if __name__ == "__main__":
    run(create)