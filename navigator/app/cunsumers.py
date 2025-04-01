import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ScheduleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Send initial data
        await self.send_initial_data()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'day_of_week':
            day = data.get('day')
            schedules = await self.get_schedule_for_day(day)

            response = {
                'action': 'init',
                'schedules': schedules,
                'error': '0' if schedules else '1'
            }
            await self.send(text_data=json.dumps(response))

    async def send_initial_data(self):
        # Send empty initial data
        await self.send(text_data=json.dumps({
            'action': 'init',
            'schedules': {},
            'error': '1'
        }))

    async def get_schedule_for_day(self, day):
        mock_data = {
            '8а_пн': {
                '1': ['8а', '8а', 'Группа 1', 'Иванов, Петров', 'Математика', 'Иванова А.А.', '101',
                      'https://zoom.us/123', '', ''],
                '2': ['8а', '8а', 'Группа 2', 'Сидоров, Кузнецов', 'Физика', 'Петров Б.Б.', '202',
                      'https://zoom.us/456', 'Смирнов В.В.', 'https://zoom.us/789']
            },
            '8а_вт': {
                '1': ['8а', '8а', 'Группа 1', 'Иванов, Петров', 'Литература', 'Сидорова Г.Г.', '305',
                      'https://zoom.us/111', '', ''],
                '3': ['8а', '8а', 'Группа 1', 'Иванов, Петров', 'История', 'Кузнецов Д.Д.', '404',
                      'https://zoom.us/222', '', '']
            }
        }

        return mock_data.get(day, {})
