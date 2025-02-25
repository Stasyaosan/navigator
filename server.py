import websockets
import asyncio
import json

clients = set()


async def handler(websocket):
    global schedules
    clients.add(websocket)

    try:
        await websocket.send(json.dumps({"action": "init", "schedules": schedules}))

        async for message in websocket:
            data = json.loads(message)

            if data["action"] == "add":
                new_id = max([s["id"] for s in schedules] or [0]) + 1
                new_schedule = {"id": new_id, "subject": data["subject"], "time": data["time"]}
                schedules.append(new_schedule)

            elif data["action"] == "update":
                for s in schedules:
                    if s["id"] == data["id"]:
                        s["subject"] = data["subject"]
                        s["time"] = data["time"]

            elif data["action"] == "delete":
                schedules = [s for s in schedules if s["id"] != data["id"]]

            response = json.dumps({"action": "update", "schedules": schedules})
            await asyncio.gather(*(client.send(response) for client in clients))

    except websockets.ConnectionClosed:
        pass

    finally:
        clients.remove(websocket)


async def main():
    server = await websockets.serve(handler, 'localhost', 8765)
    print('Websockets-сервер запущен')
    await server.wait_closed()


asyncio.run(main())
