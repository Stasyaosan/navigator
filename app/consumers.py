import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class ScheduleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
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

    @sync_to_async
    def get_schedules(self, class_name, day_of_week):
        import django
        django.setup()

        from app.models import Schedule
        from django.db.models import Q
        data = Schedule.objects.filter(Q(class_room=class_name) & Q(day_of_week=day_of_week)).order_by('time')
        r = {}
        r[f'{class_name}_{day_of_week}'] = {}
        for d in data:
            r[f'{class_name}_{day_of_week}'][d.time] = [d.class_room,d.day_of_week,d.forma,d.students, d.subject, d.teacher, d.cabinet, d.link, d.replace_teacher, d.replace_link]

        return r
    async def get_schedule_for_day(self, day):
        class_name, day_of_week = day.split('_')
        data = await self.get_schedules(class_name, day_of_week)

        return data.get(day, {})
