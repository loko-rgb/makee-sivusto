from flask_socketio import SocketIO

socketio = SocketIO(manage_session=False, logger=False, engineio_logger=False)