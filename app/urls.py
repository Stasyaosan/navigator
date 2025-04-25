from django.urls import path
from .views import update_schedule

urlpatterns = [
    path('update_schedule', update_schedule)
]
