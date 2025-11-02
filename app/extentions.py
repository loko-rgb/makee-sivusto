from flask_socketio import SocketIO

socketio = SocketIO(manage_session=False, logger=True, engineio_logger=True)