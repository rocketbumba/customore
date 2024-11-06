from unittest.mock import patch

from rest_framework.test import APITestCase
import json

from task.enums.response_code import ResponseCode
from task.exceptions.task_exceptions import TaskNotFound
from task.models import Task


class TestUpdateTaskView(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="PENDING",
            due_date="2024-11-2"
        )

    @patch(
        'task.views.update_task_view.TaskService'
    )
    def test_update_task_success(self, mock_class_task_service):
        mock_get_task_service = mock_class_task_service.return_value
        mock_get_task_service.update_task.return_value = self.task
        url = '/task/update-task/1'
        response = self.client.post(url, data={
            "title": "Test Task Update",
            "description": "Test Description",
            "status": "COMPLETED",
            "due_date": "2024-11-2"
        })
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['response_code'], ResponseCode.SUCCESS)

    @patch(
        'task.views.update_task_view.TaskService'
    )
    def test_update_task_not_found(self, mock_class_task_service):
        mock_get_task_service = mock_class_task_service.return_value
        mock_get_task_service.update_task.side_effect = TaskNotFound()
        url = '/task/update-task/1'
        response = self.client.post(url, data={
            "title": "Test Task Update",
            "description": "Test Description",
            "status": "COMPLETED",
            "due_date": "2024-11-2"
        })
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['response_code'], ResponseCode.TASK_NOT_FOUND)