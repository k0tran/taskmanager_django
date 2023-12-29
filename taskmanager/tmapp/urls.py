from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('', lambda _: redirect('projects')),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    
    path('projects/<int:project_id>/members/', views.project_members, name='project_members'),
    path('projects/<int:project_id>/members/update/', views.members_update, name='members_update'),
    path('projects/<int:project_id>/members/delete/', views.members_delete, name='members_delete'),
    path('projects/<int:project_id>/create_task/', views.task_create, name='task_create'),
    path('projects/<int:project_id>/completed/', views.completed_tasks, name='completed_tasks'),
    path('projects/<int:project_id>/archieved/', views.archieved_tasks, name='archieved_tasks'),

    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:task_id>/update_status/', views.task_update_status, name='task_update_status'),
    path('tasks/<int:task_id>/create_comment/', views.comment_create, name='comment_create'),
    
    path('comments/<int:comment_id>/', views.comment_update, name='comment_update'),
    path('comments/<int:commen_id>/delete/', views.comment_delete, name='comment_delete'),
]