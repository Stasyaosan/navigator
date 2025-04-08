from celery import shared_task
from .parser import parser


@shared_task
def update_schedule():
    parser()
