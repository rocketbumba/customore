
from django.test import TestCase
from task.exceptions.task_exceptions import TaskNotFound
from task.models import Task, TaskStatus
from task.services.task_services import TaskService

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