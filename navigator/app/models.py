from django.db import models


class Schedule(models.Model):
    time = models.CharField(max_length=244)
    class_room = models.CharField(max_length=244)
    day_of_week = models.CharField(max_length=244)
    forma = models.CharField(max_length=244)
    students = models.TextField()
    subject = models.CharField(max_length=244)
    teacher = models.CharField(max_length=244)
    cabinet = models.CharField(max_length=244)
    link = models.CharField(max_length=244)
    replace_teacher = models.CharField(max_length=244)
    replace_link = models.CharField(max_length=244)
