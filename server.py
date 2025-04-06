import websockets
import asyncio
import json
import os

clients = set()


async def handler(websocket):
    global schedules
    clients.add(websocket)

    try:
        with open('navigator/app/json/data.json') as f:
            schedules = json.loads(f.read())
            new_schedules = {}
            for time, data in schedules.items():
                res = ''
                a = time.split(':')
                if len(a[0]) == 1:
                    res += '0' + a[0] + ':'
                else:
                    res += a[0] + ':'
                if len(a[1]) == 1:
                    res += '0' + a[1]
                else:
                    res += a[1]
                new_schedules[res] = data
            schedules = dict(sorted(new_schedules.items()))

        await websocket.send(json.dumps({"action": "init", "schedules": schedules}))

        async for message in websocket:
            data = json.loads(message)
            if data['action'] == 'day_of_week':
                if not os.path.exists(f'navigator/app/json/{data['day']}.json'):
                    await websocket.send(json.dumps({"action": "init", "schedules": '', 'error': '1'}))
                try:
                    with open(f'navigator/app/json/{data['day']}.json') as f:
                        schedules = json.loads(f.read())
                        new_schedules = {}
                        for time, data in schedules.items():
                            res = ''
                            a = time.split(':')
                            if len(a[0]) == 1:
                                res += '0' + a[0] + ':'
                            else:
                                res += a[0] + ':'
                            if len(a[1]) == 1:
                                res += '0' + a[1]
                            else:
                                res += a[1]
                            new_schedules[res] = data
                        schedules = dict(sorted(new_schedules.items()))

                    await websocket.send(json.dumps({"action": "init", "schedules": schedules, 'error': '0'}))
                except:
                    await websocket.send(json.dumps({"action": "init", "schedules": '', 'error': '2'}))

            elif data["action"] == "add":
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
