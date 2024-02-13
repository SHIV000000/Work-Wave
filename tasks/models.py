# tasks/models.py
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def user_is_project_manager(self, user):
        project_manager_group = Group.objects.get(name='Project Managers')
        return project_manager_group in user.groups.all()

    class Meta:
        app_label = 'tasks'  # Add this line


class TaskComment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='task_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'tasks'  


class Task(models.Model):
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To Do')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.ManyToManyField('TaskComment', related_name='comments', blank=True)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True)
    time_spent = models.DurationField(default=timedelta())
    category = models.ForeignKey('TaskCategory', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tasks' 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    social_links = models.ManyToManyField('SocialLink', blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    
    class Meta:
        app_label = 'tasks' 


class SocialLink(models.Model):
    platform = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.platform
    
    class Meta:
        app_label = 'tasks' 

    

class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'tasks' 


class TaskCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'tasks' 


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Add or change related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_user_permissions',
    )

    class Meta:
        app_label = 'tasks'

# Note: Groups creation moved to a separate function
@receiver(post_migrate)
def create_custom_groups(sender, **kwargs):
    from django.contrib.auth.models import Group

    # Create custom groups
    Group.objects.get_or_create(name='Project Managers')
    Group.objects.get_or_create(name='Team Leads')
    # ... (add more groups as needed)