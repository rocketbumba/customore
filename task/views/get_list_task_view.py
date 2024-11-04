from enum import Enum

from django.core.paginator import Paginator

from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from task.enums.task_status import TaskStatus
from task.exceptions.task_exceptions import UnhandledProcessTaskTransaction
from task.models import Task
from task.services.task_services import TaskService


class ResponseCode(Enum):
    SUCCESS = 'SUCCESS'
    INVALID_REQUEST = 'INVALID_REQUEST'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    TASK_NOT_FOUND = 'TASK_NOT_FOUND'


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields  = ('id', 'title', 'description', 'due_date', 'status')

class GetListTask(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()


    def get(self, request, limit:int, status_task: TaskStatus):
        try:
            list_task = self.service.get_list_task(status=status_task)
            list_task_pagination = Paginator(list_task, limit).object_list
            response_data = {
                'status': True,
                'data':OutputSerializer(list_task_pagination, many=True).data,
                'response_code': ResponseCode.SUCCESS.value,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except UnhandledProcessTaskTransaction as error:
            response_data = {
                'status': False,
                'response_code': ResponseCode.UNKNOWN_ERROR.value,
                'message': str(error)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


