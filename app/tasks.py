# tasks.py
from celery import shared_task
from .parser import parser
from .add_data import ImportToModel


@shared_task
def update_schedule():
    print('Задача парсинг json  выполняется')
    parser()
    print('Задача парсинг json выполнена')
    print('Задача парсинг модель  выполняется')
    i = ImportToModel()
    import asyncio
    asyncio.run(i.import_data_async())
    print('Задача парсинг модель выполнена')
