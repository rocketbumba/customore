
from rest_framework import serializers, status

from customore.base_api_view import BaseAPIView
from task.enums.response_code import ResponseCode
from task.enums.task_status import TaskStatus
from task.exceptions.task_exceptions import UnhandledProcessTaskTransaction
from task.services.task_services import TaskService


class InputSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField()
    due_date = serializers.DateField(format="%Y-%m-%d")
    status = serializers.CharField(default=TaskStatus.PENDING.value)



class CreateTaskView(BaseAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()


    def post(self, request):
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return self._build_response(
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
                response_code=ResponseCode.INVALID_REQUEST
            )

        try:
            self.service.create_task(serializer.validated_data)
            return self._build_response(
                success=True,
                status_code=status.HTTP_201_CREATED,
                response_code=ResponseCode.SUCCESS
            )
        except UnhandledProcessTaskTransaction:
            return self._build_response(
                success=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response_code=ResponseCode.UNKNOWN_ERROR
            )

