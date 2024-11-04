from django.db import models


class TaskStatus(models.TextChoices):
    COMPLETED = 'COMPLETED'
    PENDING = 'PENDING'

# Create your models here.
class Task(models.Model):

    title = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(max_length=1000, null=True)
    due_date = models.DateField(null=True)
    status = models.CharField(choices=TaskStatus)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



