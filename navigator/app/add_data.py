# import django
# django.setup()
from .models import Schedule
from django.db.models import Q
import os
import json
from channels.db import database_sync_to_async


class ImportToModel:
    dir_import = 'app/json'

    @database_sync_to_async
    def get_exist(self, time, data_schedule):
        if Schedule.objects.filter(
                Q(time=time) & Q(day_of_week=data_schedule[0].split('_')[1]) & Q(class_room=data_schedule[2])).exists():
            return True
        return False

    @database_sync_to_async
    def _save_schedule(self, time, data_schedule):
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

        schedule = Schedule()
        schedule.time = time
        schedule.day_of_week = data_schedule[0].split('_')[1]
        schedule.class_room = data_schedule[2]
        schedule.forma = data_schedule[1]
        schedule.students = data_schedule[3]
        schedule.subject = data_schedule[4]
        schedule.teacher = data_schedule[5]
        schedule.cabinet = data_schedule[6]
        schedule.link = data_schedule[7]
        schedule.replace_teacher = data_schedule[8]
        schedule.replace_link = data_schedule[9]
        schedule.save()

    def _update_schedule(self, time, data_schedule):
        schedule = Schedule.objects.filter(
            Q(time=time) & Q(day_of_week=data_schedule[0].split('_')[1]) & Q(class_room=data_schedule[2])).first()

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
        schedule.time = res
        schedule.day_of_week = data_schedule[0].split('_')[1]

        schedule.class_room = data_schedule[2]
        schedule.forma = data_schedule[1]
        schedule.students = data_schedule[3]
        schedule.subject = data_schedule[4]
        schedule.teacher = data_schedule[5]
        schedule.cabinet = data_schedule[6]
        schedule.link = data_schedule[7]
        schedule.replace_teacher = data_schedule[8]
        schedule.replace_link = data_schedule[9]
        schedule.save()

    async def import_data_async(self):
        print(os.getcwd())
        data = os.listdir(self.dir_import)
        for path in data:
            with open(f'{self.dir_import}/{path}') as f:
                d = json.loads(f.read())
            for time, data_schedule in d.items():
                exists = await self.get_exist(time, data_schedule)
                if not exists:
                    await self._save_schedule(time, data_schedule)
                else:
                    await self._update_schedule(time, data_schedule)
