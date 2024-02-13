# tasks/apps.py

from django.apps import AppConfig
from django.db.models.signals import post_migrate

class WorkwaveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        from .models import create_custom_groups
        post_migrate.connect(create_custom_groups, sender=self)
