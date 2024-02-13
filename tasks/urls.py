# tasks/urls.py
from django.urls import path
from .views import HomeView, CustomLoginView, CustomProfileView
from .views import project_list, project_detail, project_create, project_update, project_delete
from .views import profile_view, project_update
from .views import task_create, task_update, task_delete
from .views import add_comment, add_attachment
from .views import custom_logout


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('projects/', project_list, name='project_list'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),
    path('projects/create/', project_create, name='project_create'),
    path('projects/<int:project_id>/update/', project_update, name='project_update'),
    path('projects/<int:project_id>/delete/', project_delete, name='project_delete'),
    path('accounts/profile/', CustomProfileView.as_view(), name='profile'),
    path('profile/update/', project_update, name='project_update'),
    path('projects/<int:project_id>/tasks/create/', task_create, name='create_task'),
    path('projects/<int:project_id>/tasks/<int:task_id>/update/', task_update, name='task_update'),
    path('projects/<int:project_id>/tasks/<int:task_id>/delete/', task_delete, name='task_delete'),
    path('tasks/<int:task_id>/add-comment/', add_comment, name='add_comment'),
    path('tasks/<int:task_id>/add-attachment/', add_attachment, name='add_attachment'),
    
]

