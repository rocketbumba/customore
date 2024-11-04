from django.urls import path

from task.views.create_task_view import CreateTaskView
from task.views.get_list_task_view import GetListTaskView
from task.views.get_task_view import GetTaskView
from task.views.update_task_view import UpdateTaskView

urlpatterns = [
    path('create-task', CreateTaskView.as_view()),
    path('get-task/<int:task_id>', GetTaskView.as_view()),
    path('update-task/<int:task_id>', UpdateTaskView.as_view()),
    path('get-list-task/', GetListTaskView.as_view()),
    path('get-list-task/<int:limit>/<int:page>', GetListTaskView.as_view()),
    path('get-list-task/<int:limit>/<int:page>/<path:status_task>', GetListTaskView.as_view()),
]