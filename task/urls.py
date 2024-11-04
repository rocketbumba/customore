from django.urls import path

from task.views.create_task_view import CreateTaskView
from task.views.get_list_task_view import GetListTask
from task.views.get_task_view import GetTask
from task.views.update_task_view import UpdateTaskView

urlpatterns = [
    path('create-task', CreateTaskView.as_view()),
    path('get-task/<int:task_id>', GetTask.as_view()),
    path('update-task/<int:task_id>', UpdateTaskView.as_view()),
    path('get-list-task/', GetListTask.as_view()),
    path('get-list-task/<int:limit>/', GetListTask.as_view()),
    path('get-list-task/<path:status_task>/', GetListTask.as_view()),
    path('get-list-task/<int:limit>/<path:status_task>', GetListTask.as_view()),
]