
from rest_framework import serializers, status
from rest_framework.request import Request

from customore.base_api_view import BaseAPIView
from task.enums.response_code import ResponseCode
from task.exceptions.task_exceptions import TaskNotFound, UnhandledProcessTaskTransaction
from task.models import TaskStatus
from task.services.task_services import TaskService


class InputSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=False)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField(required=False)
    status = serializers.ChoiceField(required=False, choices=TaskStatus.choices)



class UpdateTaskView(BaseAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()

    def post(self, request: Request, task_id: int):
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return self._build_response(
                success=False,
                response_code=ResponseCode.INVALID_REQUEST,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            self.service.update_task(task_id=task_id, task_data=serializer.validated_data)
            return self._build_response(
                success=True,
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





