
from django.core.paginator import Paginator

from rest_framework import status, serializers

from customore.base_api_view import BaseAPIView
from task.enums.response_code import ResponseCode
from task.enums.task_status import TaskStatus
from task.exceptions.task_exceptions import UnhandledProcessTaskTransaction
from task.models import Task
from task.services.task_services import TaskService


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields  = ('id', 'title', 'description', 'due_date', 'status')

class GetListTaskView(BaseAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()


    def get(self, request, limit: int = None, page: int = None ,status_task: TaskStatus=None):
        try:
            list_task = self.service.get_list_task(status=status_task)
            if limit is None:
                limit = 5
            list_task_pagination = Paginator(list_task, limit)
            data = OutputSerializer(list_task_pagination.get_page(page), many=True).data
            return self._build_list_response(
                success=True,
                status_code=status.HTTP_200_OK,
                response_code=ResponseCode.SUCCESS,
                data=data,
                total_page=list_task_pagination.num_pages,
            )
        except UnhandledProcessTaskTransaction:
            return self._build_response(
                success=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response_code=ResponseCode.UNKNOWN_ERROR
            )


