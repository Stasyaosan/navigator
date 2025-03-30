from django.shortcuts import render


def schedule(request, room_name):
    return render(request, 'schedule.html', {'room_name': room_name})
