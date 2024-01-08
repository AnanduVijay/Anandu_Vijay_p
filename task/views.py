from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    return render(request, "home.html")


# Authentication Users
def singnup_user(request):
    """
    Create new user using UserCreationForm 
    """
    if request.method == "GET":
        return render(request, "signupuser.html", {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("alltasks")
            except IntegrityError:
                return render(
                    request,
                    "signupuser.html",
                    {
                        "form": UserCreationForm(),
                        "error": "That username has already been taken. Please choose a new username",
                    },
                )
        else:
            return render(
                request,
                "signupuser.html",
                {
                    "form": UserCreationForm(),
                    "error": "Passwords did not match",
                },
            )


def login_user(request):
    """
    Help user to login and redirect to list of all tasks
    """
    if request.method == "GET":
        return render(
            request, "loginuser.html", {"form": AuthenticationForm()}
        )
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "loginuser.html",
                {
                    "form": AuthenticationForm(),
                    "error": "username and password do not match",
                },
            )
        else:
            login(request, user)
            return redirect("alltasks")


@login_required
def logout_user(request):
    """
    Logout the user and redirect to the hompage
    """
    if request.method == "POST":
        logout(request)
        return redirect("homepage")

# CRUD operations for TASk
@login_required
def task_list(request):
    """
    List all the uncompleted tasks in the order of due_date
    """
    tasks = Task.objects.filter(
        user=request.user, date_completed__isnull=True
    ).order_by("due_date")
    return render(request, "tasklist.html", {"tasks": tasks})


@login_required
def create_task(request):
    """
    Provide TaskForm to create new task and on save
    redirect to alltasks
    """
    if request.method == "POST":
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                print(task.title)
                return redirect("alltasks")
        except ValueError:
            return render(
                request,
                "createtask.html",
                {
                    "form": TaskForm(),
                    "error": "Bad data passed in. Try again.",
                },
            )
    else:
        form = TaskForm()
    return render(request, "createtask.html", {"form": form})


@login_required
def edit_task(request, task_pk):
    """
    Give Taskform of that choosen task and can edit it and save
    """
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == "GET":
        form = TaskForm(instance=task)
        return render(request, "edittask.html", {"task": task, "form": form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("alltasks")
        except ValueError:
            return render(
                request,
                "edittask.html",
                {"task": task, "form": form, "error": "Bad info"},
            )


@login_required
def complete_task(request, task_pk):
    """
    Can Update a task after Completing and it save
    with completed date 
    """
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == "POST":
        task.date_completed = timezone.now()
        task.save()
        return redirect("alltasks")


@login_required
def delete_task(request, task_pk):
    """
    Delete a specific task and redirect to alltasks
    """
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    print(request.method)
    if request.method == "POST":
        task.delete()
        return redirect("alltasks")
