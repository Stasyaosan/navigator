# tasks.py
from celery import shared_task
from .parser import parser

@shared_task
def update_schedule():
    print('Задача выполняется')
    parser()
    print('Задача выполнена')