from unittest.mock import patch

from rest_framework.test import APITestCase
import json

from task.enums.response_code import ResponseCode
from task.exceptions.task_exceptions import TaskNotFound
from task.models import Task


class TestGetTaskView(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="PENDING",
            due_date="2024-11-2"
        )

    @patch(
        'task.views.get_task_view.TaskService'
    )
    def test_get_task_success(self, mock_class_task_service):
        mock_get_task_service = mock_class_task_service.return_value
        mock_get_task_service.get_task.return_value = self.task
        url = '/task/get-task/1'
        response = self.client.get(url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['response_code'], ResponseCode.SUCCESS)

    @patch(
        'task.views.get_task_view.TaskService'
    )
    def test_get_task_not_found_view(
            self, mock_class_task_service
    ):
        mock_get_task_service = mock_class_task_service.return_value
        mock_get_task_service.get_task.side_effect = TaskNotFound()
        url = '/task/get-task/1'
        response = self.client.get(url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['success'], False)