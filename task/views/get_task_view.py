from enum import Enum

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from task.exceptions.task_exceptions import TaskNotFound
from task.models import Task
from task.services.task_services import TaskService


class ResponseCode(Enum):
    SUCCESS = 'SUCCESS'
    INVALID_REQUEST = 'INVALID_REQUEST'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    TASK_NOT_FOUND = 'TASK_NOT_FOUND'

class OutPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields  = ('id', 'title', 'description', 'due_date', 'status')

class GetTask(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()

    def get(self, request, task_id):

        try:
            task = self.service.get_task(task_id)
            response_data = {
                'status': True,
                'data': OutPutSerializer(task).data,
                'response_code': ResponseCode.SUCCESS.value,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except TaskNotFound:
            response_data = {
                'status': False,
                'response_code': ResponseCode.TASK_NOT_FOUND.value,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)



