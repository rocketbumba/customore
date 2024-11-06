from unittest.mock import patch

from rest_framework.test import APITestCase
import json

from task.enums.response_code import ResponseCode
from task.models import Task

class TestCreateTaskView(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="PENDING",
            due_date="2024-11-2"
        )

    @patch(
        'task.views.create_task_view.TaskService'
    )
    def test_create_task_success(self, mock_class_task_service):
        mock_get_task_service = mock_class_task_service.return_value
        mock_get_task_service.create_task.return_value = self.task
        url = '/task/create-task'
        response = self.client.post(url, data={
            "title": "Test Task 1",
            "description": "Test Description",
            "status": "PENDING",
            "due_date": "2024-11-2"
        })
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['response_code'], ResponseCode.SUCCESS)

    @patch(
        'task.views.create_task_view.TaskService'
    )
    def test_create_task_without_title(self,mock_class_task_service ):
        mock_get_task_service = mock_class_task_service.return_value
        mock_get_task_service.create_task.return_value = self.task
        url = '/task/create-task'
        response = self.client.post(url, data={
            "description": "Test Description",
            "status": "PENDING",
            "due_date": "2024-11-2"
        })
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['response_code'], ResponseCode.INVALID_REQUEST)

    @patch(
        'task.views.create_task_view.TaskService'
    )
    def test_create_task_with_title_blank(self, mock_class_task_service):
        mock_get_task_service = mock_class_task_service.return_value
        mock_get_task_service.create_task.return_value = self.task
        url = '/task/create-task'
        response = self.client.post(url, data={
            "title": "",
            "description": "Test Description",
            "status": "PENDING",
            "due_date": "2024-11-2"
        })
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['response_code'], ResponseCode.INVALID_REQUEST)