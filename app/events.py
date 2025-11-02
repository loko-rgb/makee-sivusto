from .extentions import socketio
from random import shuffle
from flask_socketio import emit, join_room, close_room, leave_room
from flask import request, render_template, session
import pandas as pd
import time


cards = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4), (5, 1), (5, 2), (5, 3), (5, 4), (6, 1), (6, 2), (6, 3), (6, 4), (7, 1), (7, 2), (7, 3), (7, 4), (8, 1), (8, 2), (8, 3), (8, 4), (9, 1), (9, 2), (9, 3), (9, 4), (10, 1), (10, 2), (10, 3), (10, 4), (11, 1), (11, 2), (11, 3), (11, 4), (12, 1), (12, 2), (12, 3), (12, 4), (13, 1), (13, 2), (13, 3), (13, 4), (14, 1), (14, 2), (14, 3), (14, 4)]
db2 = pd.read_csv("/Users/lukakopeykin/documents/python/Flask app 2/app/games.csv", sep=",")

@socketio.on("connect")
def connect():
    print(f"User at {request.sid} connected")

@socketio.on("start")
def start():
    global db2

    if db2.loc[db2["sid"] == request.sid].empty == True:
        db2 = db2[db2["sid"] != request.sid]
        print(f"User at {request.sid} closed game")
        time.sleep(1)

    list_of_cards_loc = list(range(0, 56))
    shuffle(list_of_cards_loc)
    db2.loc[len(db2)] = {"#":len(db2)+1,"sid":request.sid,"cards":list_of_cards_loc}
    db2.to_csv("games.csv", index=False)

    print(f"User at {request.sid} started game")

    


@socketio.on("disconnect")
def disconnect():
    global db2
    if db2.loc[db2["sid"] == request.sid].empty != True:
        db2 = db2[db2["sid"] != request.sid]
        db2.to_csv("/Users/lukakopeykin/Documents/Python/Scripts/app/games.csv", index=False)
        print(f"User at {request.sid} closed game")


    print(f"User at {request.sid} disconnected")
