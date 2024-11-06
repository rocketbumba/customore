
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response

from customore.base_api_view import BaseAPIView
from task.enums.response_code import ResponseCode
from task.exceptions.task_exceptions import TaskNotFound, UnhandledProcessTaskTransaction
from task.models import Task
from task.services.task_services import TaskService


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields  = ('id', 'title', 'description', 'due_date', 'status')

class GetTaskView(BaseAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()

    def get(self, request: Request, task_id: int):

        try:
            task = self.service.get_task(task_id=task_id)
            return self._build_response(
                success=True,
                data=OutputSerializer(task).data,
                response_code=ResponseCode.SUCCESS,
                status_code=status.HTTP_200_OK,
            )
        except TaskNotFound:
            return self._build_response(
                success=False,
                response_code=ResponseCode.TASK_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except UnhandledProcessTaskTransaction:
            return self._build_response(
                success=False,
                response_code=ResponseCode.UNKNOWN_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



