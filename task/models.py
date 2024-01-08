from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models


def one_week_from():
    return timezone.now() + timezone.timedelta(days=7)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(default=one_week_from)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date_completed = models.DateTimeField(null=True, blank=True)


def __str__(self):
    return self.title
