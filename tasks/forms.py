# tasks/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Project, Task, Profile, TaskComment, TaskAttachment, TaskCategory
from .models import TaskCategory
from django.forms.widgets import DateInput


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "due_date",
            "status",
            "project",
            "assigned_to",
            "category",
        ]
        widgets = {
            "due_date": DateInput(attrs={"type": "date"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "start_date", "end_date"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["social_links", "bio", "profile_image"]


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ["comment"]


class TaskAttachmentForm(forms.ModelForm):
    class Meta:
        model = TaskAttachment
        fields = ["file"]


class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ["name"]
