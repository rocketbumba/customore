from enum import Enum

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from task.exceptions.task_exceptions import TaskNotFound, UnhandledProcessTaskTransaction
from task.services.task_services import TaskService


class InputSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField(required=False)
    status = serializers.CharField(required=False)

class ResponseCode(Enum):
    SUCCESS = 'SUCCESS'
    INVALID_REQUEST = 'INVALID_REQUEST'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    TASK_NOT_FOUND = 'TASK_NOT_FOUND'


class UpdateTaskView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()

    def post(self, request, task_id):
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            response_date = {
                'success': False,
                'response_code': ResponseCode.INVALID_REQUEST.value,
            }
            return Response(data=response_date, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.service.update_task(task_id=task_id, task_data=serializer.validated_data)
            response_data = {
                'success': True,
                'response_code': ResponseCode.SUCCESS.value,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except TaskNotFound:
            response_data = {
                'success': False,
                'response_code': ResponseCode.TASK_NOT_FOUND.value,

            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)
        except UnhandledProcessTaskTransaction as error:
            response_data = {
                'success': False,
                'response_code': ResponseCode.UNKNOWN_ERROR.value,
                'message': str(error),
            }
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




