#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
from enum import Enum
from collections import defaultdict
from typing import Dict
import websockets
from jill_box.game import GameGateway, Room, StartReturnCodes, InteractReturnCodes, JoinReturnCodes
from jill_box.game_test import TestRoom
logging.basicConfig()

USERS: Dict[str, Dict[str, websockets.WebSocketServerProtocol]] = defaultdict(dict)

GATEWAY = GameGateway()

class ClientServerMsgs(Enum):
    create_room = 'create_room'
    join_room = 'join_room'
    start_room = 'start_room'
    submit_prompt = 'submit_prompt'
    submit_vote = 'submit_vote'


class ServerClientMsgs(Enum):
    error = 'error'
    join_room = 'join_room'
    user_update = 'user_update'
    ask_prompt = 'ask_prompt'
    ask_vote = 'ask_vote'
    show_results = 'show_results'
    game_done = 'game_done'


async def send_error(websocket, error):
    await websocket.send(json.dumps({"type": ServerClientMsgs.error.value, "msg": error.name}))

async def notify_new_users(room):
    if len(USERS.get(room,{})) > 1: # notify about new users
        messages = {}
        for user in USERS[room].keys():
            others = [ other for other in USERS[room].keys() if other != user ]
            messages[user] = json.dumps({"type": ServerClientMsgs.user_update.value, "users": others })
        print(messages)
        await asyncio.wait([v.send(messages[k]) for k, v in USERS[room].items()])


async def send_answers(room):
    messages = {}
    for user in USERS[room].keys():
        _, _, answers = GATEWAY.get_room_state(room, user)
        answers = json.loads(answers)
        messages[user] = json.dumps({"type": ServerClientMsgs.ask_vote.value, "answers": answers })
    print(messages)
    await asyncio.wait([v.send(messages[k]) for k, v in USERS[room].items()])

async def send_results(room):
    ret, _, results = GATEWAY.get_room_state(room)
    results = json.loads(results)
    message = json.dumps({"type": ServerClientMsgs.show_results.value, "results": results})
    print(ret)
    print(message)
    await asyncio.wait([v.send(message) for v in USERS[room].values()])

async def send_prompt(room):
    ret, _, prompt = GATEWAY.get_room_state(room)
    message = json.dumps({"type": ServerClientMsgs.ask_prompt.value, "prompt": prompt})
    print(ret)
    print(message)
    await asyncio.wait([v.send(message) for v in USERS[room].values()])

async def start_next_round(room):
    for user in USERS[room].keys():
        GATEWAY.submit_data(room, user, {})
    ret, state, _ = GATEWAY.get_room_state(room)
    print(ret)
    print(state)
    if TestRoom.State(state) == TestRoom.State.COLLECTING_ANSWERS:
        await asyncio.sleep(20)
        await send_prompt(room)
    else:
        message = json.dumps({"type": ServerClientMsgs.game_done.value})
        await asyncio.wait([v.send(message) for v in USERS[room].values()])

async def counter(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print(data,1)
        if ClientServerMsgs(data['type']) == ClientServerMsgs.create_room:
            room = GATEWAY.new_game(TestRoom)
            data['type'] = ClientServerMsgs.join_room.value
            data['room'] = room
        if ClientServerMsgs(data['type']) == ClientServerMsgs.join_room:
            ret = GATEWAY.join_room(data['room'], data['user'])
            if ret == JoinReturnCodes.SUCCESS:
                await websocket.send(json.dumps(data))
                USERS[data['room']][data['user']] = websocket
                await notify_new_users(data['room'])
            else:
                await send_error(websocket ,ret)           
        if ClientServerMsgs(data['type']) == ClientServerMsgs.start_room:
            ret = GATEWAY.room_start(data['room'])
            if ret == StartReturnCodes.SUCCESS:
                await send_prompt(data['room'])
            else:
                await send_error(websocket, ret)    
        if ClientServerMsgs(data['type']) == ClientServerMsgs.submit_prompt:
            ret = GATEWAY.submit_data(data['room'], data['user'], data)
            if ret == InteractReturnCodes.SUCCESS:
                ret, state, _ = GATEWAY.get_room_state(data['room'])
                print(ret)
                print(state)
                if TestRoom.State.VOTING == TestRoom.State(state):
                    await send_answers(data['room'])
            else:
                await send_error(websocket, ret)
        if ClientServerMsgs(data['type']) == ClientServerMsgs.submit_vote:
            ret = GATEWAY.submit_data(data['room'], data['user'], data)
            if ret == InteractReturnCodes.SUCCESS:
                ret, state, _ = GATEWAY.get_room_state(data['room'])
                print(ret)
                print(state)
                if TestRoom.State.SHOWING_RESULTS == TestRoom.State(state):
                    await send_results(data['room'])
                    asyncio.ensure_future(start_next_round(data['room']))
            else:
                await send_error(websocket, ret)  

start_server = websockets.serve(counter, "192.168.1.110", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
