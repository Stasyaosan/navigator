import json
from channels.generic.websocket import AsyncWebsocketConsumer
import django
from asgiref.sync import sync_to_async
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navigator.settings')
django.setup()
from .models import Schedule
from django.db.models import Q


class ScheduleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_initial_data()

    async def disconnect(self, close_code):
        pass

    @sync_to_async
    def save_message(self, d):
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

    @sync_to_async
    def get_schedules(self, class_name, day_of_week):
        data = Schedule.objects.filter(Q(class_room=class_name) & Q(day_of_week=day_of_week)).order_by('time')
        r = {}
        r[f'{class_name}_{day_of_week}'] = {}
        for d in data:
            r[f'{class_name}_{day_of_week}'][d.time] = [d.class_room, d.day_of_week, d.forma, d.students, d.subject,
                                                        d.teacher, d.cabinet, d.link, d.replace_teacher, d.replace_link]

        return r

    async def get_schedule_for_day(self, day):
        class_name, day_of_week = day.split('_')
        data = await self.get_schedules(class_name, day_of_week)
        print(data)
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
        return data.get(day, {})
