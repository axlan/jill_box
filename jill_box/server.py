#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
from collections import defaultdict
from typing import Dict
import websockets
from jill_box.game import GameGateway, Room, StartReturnCodes, InteractReturnCodes, JoinReturnCodes
from jill_box.game_test import TestRoom
logging.basicConfig()

USERS: Dict[str, Dict[str, websockets.WebSocketServerProtocol]] = defaultdict(dict)

GATEWAY = GameGateway()


async def notify_new_users(room):
    if len(USERS.get(room,{})) > 1: # notify about new users
        messages = {}
        for user in USERS[room]:
            others = [ other for other in USERS[room].keys() if other != user ]
            messages[user] = json.dumps({"type": "user_update", "users": others })
        print(messages)
        await asyncio.wait([v.send(messages[k]) for k, v in USERS[room].items()])

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    #await register(websocket)
    try:
        #await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            print(data)
            if data['type'] == 'create_room':
                room = GATEWAY.new_game(TestRoom)
                data['type'] = 'join_room'
                data['room'] = room
            if data['type'] == 'join_room':
                ret = GATEWAY.join_room(data['room'], data['user'])
                if ret == JoinReturnCodes.ROOM_NOT_FOUND:
                    await websocket.send(json.dumps({"type": "error", "msg": 'ROOM_NOT_FOUND'}))
                elif ret == JoinReturnCodes.NAME_IN_USE:
                    await websocket.send(json.dumps({"type": "error", "msg": 'NAME_IN_USE'}))
                else:
                    await websocket.send(json.dumps(data))
                    USERS[data['room']][data['user']] = websocket
                    await notify_new_users(data['room'])
    finally:
        #await unregister(websocket)
        pass


start_server = websockets.serve(counter, "192.168.1.110", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
