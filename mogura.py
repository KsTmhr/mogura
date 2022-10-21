import asyncio
import websockets
import json

async def mogura():
    #async with websockets.connect("ws://192.168.1.224:8765") as websocket:
    #async with websockets.connect("ws://localhost:8765", ping_interval=None) as websocket:
    async with websockets.connect("ws://10.0.1.3:8765", ping_interval=None) as websocket:

        await websocket.send(json.dumps({"type": "mogura", "data": 1}))
        message = await websocket.recv()
        print(message)

        while 1:
            score = int(input("score:"))
            await websocket.send(json.dumps({"type": "score", "data":score}))
            message = await websocket.recv()
            print(message)


asyncio.run(mogura())
