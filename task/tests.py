from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APITestCase
import json

import task
from task.enums.response_code import ResponseCode
from task.exceptions.task_exceptions import TaskNotFound
from task.models import Task, TaskStatus
from task.services.task_services import TaskService


# Create your tests here.


class TestServiceTask(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="PENDING",
            due_date="2024-11-2"
        )
        self.service = TaskService()

    def test_get_task_not_found(self):
        with self.assertRaises(TaskNotFound):
            self.service.get_task(self.task.id + 1)

    def test_get_task_success(self):
        task = self.service.get_task(self.task.id)
        self.assertEqual(task.title, self.task.title)

    def test_create_task_success(self):
        task_data = {
            "title": "Test Task 1",
            "description": "Test Description",
            "status": "PENDING",
            "due_date": "2024-11-2"
        }
        task = self.service.create_task(task_data)
        self.assertEqual(task.title, task_data["title"])

    def test_update_task_success(self):
        task_data = {
            "title": "Test Task Update",
            "description": "Test Description",
            "status": "PENDING",
            "due_date": "2024-11-2"
        }
        task = self.service.update_task(task_id=self.task.id, task_data=task_data)
        self.assertEqual(task_data["title"], task.title)



    def test_update_task_not_found(self):
        with self.assertRaises(TaskNotFound):
            self.service.get_task(self.task.id + 1)

    def test_get_list_task_success(self):
        for i in range(0, 15):
            if i % 2 != 0:
                task_data_odd = {
                    "title": "Test Task 1",
                    "description": "Test Description",
                    "status": "PENDING",
                    "due_date": "2024-11-2"
                }
                task = self.service.create_task(task_data_odd)
            else:
                task_data_even = {
                    "title": "Test Task 1",
                    "description": "Test Description",
                    "status": "COMPLETED",
                    "due_date": "2024-11-2"
                }
                task = self.service.create_task(task_data_even)

        list_task = self.service.get_list_task()
        self.assertEqual(len(list_task), 16)

        list_task_pending = self.service.get_list_task(TaskStatus.PENDING)
        self.assertEqual(len(list_task_pending), 8)

        list_task_completed = self.service.get_list_task(TaskStatus.COMPLETED)
        self.assertEqual(len(list_task_completed), 8)


class TestGetTestView(APITestCase):
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

    # @patch(
    #     'task.views.update_task_view.TaskService'
    # )
    # def test_update_task_with_title_blank(self, mock_class_task_service):
    #     mock_get_task_service = mock_class_task_service.return_value
    #     url = '/task/update-task/2'
    #     response = self.client.post(url, data={
    #         # "title": "",
    #         "description": "Test Description",
    #         "status": "COMPLETED",
    #         "due_date": "2024-11-2"
    #     })
    #     data = json.loads(response.content.decode('utf-8'))
    #     self.assertEqual(data['response_code'], ResponseCode.INVALID_REQUEST)





