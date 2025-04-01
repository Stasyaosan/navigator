from django.urls import path
from .views import *

urlpatterns = [
    path('update_schedule', update_schedule),
]
