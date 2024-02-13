#tasks/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseForbidden
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskCommentForm
from .forms import TaskAttachmentForm
from .models import TaskAttachment
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone
from .models import Project, Task, TaskCategory
from .forms import ProjectForm, TaskForm, ProfileForm, TaskCommentForm, TaskAttachmentForm
from django.template import engines
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


class HomeView(TemplateView):
    template_name = 'tasks/home.html'


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


def custom_logout(request):
    LogoutView.as_view()(request)
    return redirect('login')


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tasks/project_list.html', {'projects': projects})



def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    # Task Due Notifications
    due_tasks = tasks.filter(due_date__lte=timezone.now(), status='To Do')
    upcoming_tasks = tasks.filter(due_date__gt=timezone.now(), status='To Do')

    # Task Filtering and Sorting
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    category_filter = request.GET.get('category')
    order_by = request.GET.get('order_by', '-due_date')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if category_filter:
        tasks = tasks.filter(category=category_filter)

    tasks = tasks.order_by(order_by)

    categories = TaskCategory.objects.all()

    return render(request, 'tasks/project_detail.html', {
        'project': project,
        'tasks': tasks,
        'due_tasks': due_tasks,
        'upcoming_tasks': upcoming_tasks,
        'categories': categories,
    })

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            owner_instance = request.user if request.user.is_authenticated else None
            project = form.save(commit=False)
            project.owner = owner_instance
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'tasks/project_form.html', {'form': form})


def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/project_form.html', {'form': form, 'action': 'Update'})


def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('project_list')

class CustomProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        # Add more context data as needed based on your model structure
        return context


def profile_view(request):
    return render(request, 'tasks/profile.html', {'user': request.user})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm

def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'tasks/project_form.html', {'form': form, 'action': 'Update'})



def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create', 'project': project})


def task_update(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update', 'project': project})


def task_delete(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)

    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', project_id=project.id)

    return render(request, 'tasks/task_confirm_delete.html', {'task': task, 'project': project})

def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
    return redirect('task_detail', task_id=task_id)


def add_attachment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            attachment.save()
    return redirect('task_detail', task_id=task_id)

