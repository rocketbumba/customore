from enum import Enum

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from task.enums.task_status import TaskStatus
from task.exceptions.task_exceptions import TaskNotFound
from task.models import Task
from task.services.task_services import TaskService


class InputSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField()
    due_date = serializers.DateField(format="%Y-%m-%d")
    status = serializers.CharField(default=TaskStatus.PENDING.value)




# Create your views here.


