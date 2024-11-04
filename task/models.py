from django.db import models



# Create your models here.
class Task(models.Model):
    class TaskStatus(models.TextChoices):
        COMPLETED = 'COMPLETED'
        PENDING = 'PENDING'

    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1000)
    due_date = models.DateField()
    status = models.CharField(choices=TaskStatus)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



