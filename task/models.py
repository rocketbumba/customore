from django.db import models

from task.enums.task_status import TaskStatus


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    due_date = models.DateField()
    status = models.CharField(choices=TaskStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



