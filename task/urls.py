from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="homepage"),
    path("task/create", views.create_task, name="createtask"),
    path("task/all", views.task_list, name="alltasks"),
    path("task/<int:task_pk>", views.edit_task, name="edittask"),
    path(
        "task/<int:task_pk>/complete", views.complete_task, name="completetask"
    ),
    path("task/<int:task_pk>/delete", views.delete_task, name="deletetask"),
    # AUTHENTICATION
    path("signup", views.singnup_user, name="signup"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
]
