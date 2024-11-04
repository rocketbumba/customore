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

class ResponseCode(Enum):
    SUCCESS = 'SUCCESS'
    INVALID_REQUEST = 'INVALID_REQUEST'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    TASK_NOT_FOUND = 'TASK_NOT_FOUND'



class CreateTask(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()


    def post(self, request):
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            response_data =  {
                'status': False,
                'response_code': ResponseCode.INVALID_REQUEST.value
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.service.create_task(serializer.validated_data)
            response_data = {
                'status': True,
                'response_code': ResponseCode.SUCCESS.value

            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'status': False,
                'response_code': ResponseCode.UNKNOWN_ERROR.value,
                'message': str(e)
            }
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

