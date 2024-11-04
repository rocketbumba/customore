from typing import List

from django.db import transaction

from task.enums.task_status import TaskStatus
from task.exceptions.task_exceptions import TaskNotFound, UnhandledProcessTaskTransaction
from task.models import Task


class TaskService:
    def __init__(self):
        pass

    @transaction.atomic
    def get_task(self, task_id: int) -> Task:
        return self.__get_task(task_id=task_id)

    @staticmethod
    def __get_task(task_id: int) -> Task:
        try:
            return Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise TaskNotFound()
        except Exception as e:
            raise UnhandledProcessTaskTransaction(e)

    @transaction.atomic
    def create_task(self, task_data: dict) -> Task:
        return self.__create_task(task_data)

    @staticmethod
    def __create_task(task_data: dict) -> Task:
        try:
            return Task.objects.create(
                title=task_data.get('title'),
                description=task_data.get('description'),
                due_date=task_data.get('due_date'),
                status=task_data.get('status'),
            )
        except Exception as error:
            raise UnhandledProcessTaskTransaction(error)

    @transaction.atomic
    def update_task(self, task_id: int, task_data: dict) -> Task:
        return self.__update_task(task_id=task_id, task_data=task_data)

    @staticmethod
    def __update_task(task_id: int, task_data: dict) -> Task:
        try:
            task_need_to_be_updated = Task.objects.get(pk=task_id)
            if task_data.get('title'):
                task_need_to_be_updated.title = task_data.get('title')
            if task_data.get('description'):
                task_need_to_be_updated.description = task_data.get('description')
            if task_data.get('due_date'):
                task_need_to_be_updated.due_date = task_data.get('due_date')
            if task_data.get('status'):
                task_need_to_be_updated.status = task_data.get('status')
            task_need_to_be_updated.save()
            return task_need_to_be_updated
        except Task.DoesNotExist:
            raise TaskNotFound()
        except Exception as error:
            raise UnhandledProcessTaskTransaction(error)

    def get_list_task(self, status: TaskStatus = None) -> List[Task]:
        return self.__get_list_task(status=status)

    @staticmethod
    def __get_list_task(status: TaskStatus = None) -> List[Task]:
        if status is not None:
            try:
                list_task = Task.objects.filter(status=status)
                return list_task
            except Exception as error:
                raise UnhandledProcessTaskTransaction(error)
        else:
            list_task = Task.objects.filter()
            return list_task
