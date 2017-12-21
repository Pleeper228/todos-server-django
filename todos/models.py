import datetime
from django.utils import timezone
from django.db import models

# Create your models here.

class List_Task(models.Model):
    list_task_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.list_task_text


class List_Item(models.Model):
    list_task = models.ForeignKey(List_Task, on_delete=models.CASCADE, related_name = 'items')
    list_item_text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.list_item_text
