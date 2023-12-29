from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import Project, ProjectRoles, Task, Comment
from datetime import datetime

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('projects')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect('projects')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def projects(request):
    user = request.user

    if request.method == 'POST':
        title = request.POST.get('title')

        project = Project.objects.create(title=title)
        ProjectRoles.objects.create(project=project, user=user, role=ProjectRoles.UserRole.ADMIN)

        return redirect('project_detail', project.id)

    user = request.user
    username = user.username
    project_roles = ProjectRoles.objects.filter(user=user)
    projects = Project.objects.filter(projectroles__in=project_roles)

    context = {
        'username': username,
        'projects': projects
    }

    return render(request, 'projects.html', context)

@login_required
def project_detail(request, project_id):
    user = request.user
    username = user.username
    project = Project.objects.get(id=project_id)
    is_admin = ProjectRoles.objects.get(user=user, project=project).role == ProjectRoles.UserRole.ADMIN

    if request.method == 'POST' and is_admin: 
        project.description = request.POST.get('description')
        project.save()
        return redirect('project_detail', project.id)

    tasks = Task.objects.filter(project=project, status=Task.Status.INPROGRESS)

    context = {
        'username': username,
        'project': project,
        'is_admin': is_admin,
        'tasks': tasks,
        'priorities': Task.Priority,
        'statuses': Task.Status,
    }

    return render(request, 'project_detail.html', context)

@require_POST
@login_required
def project_delete(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)
    is_admin = ProjectRoles.objects.get(user=user, project=project).role == ProjectRoles.UserRole.ADMIN

    if is_admin:
        project.delete()

    return redirect('projects')

@login_required
def project_members(request, project_id):
    user = request.user
    username = user.username
    project = Project.objects.get(id=project_id)
    is_admin = ProjectRoles.objects.get(user=user, project=project).role == ProjectRoles.UserRole.ADMIN
    roles = ProjectRoles.objects.filter(project=project)
    
    context = {
        'username': username,
        'project': project,
        'roles': roles,
        'is_admin': is_admin,
        'roles_constants': ProjectRoles.UserRole,
    }

    return render(request, 'members.html', context)

@require_POST
@login_required
def members_update(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)
    is_admin = ProjectRoles.objects.get(user=user, project=project).role == ProjectRoles.UserRole.ADMIN

    if is_admin:
        username = request.POST.get('username')
        if username.startswith('@'):
            username = username[1:]
        role = request.POST.get('role')
    
        new_user = User.objects.get(username=username)
        ProjectRoles.objects.update_or_create(project=project, user=new_user, defaults={'role': role})

    return redirect('project_members', project_id)

@require_POST
@login_required
def members_delete(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)
    is_admin = ProjectRoles.objects.get(user=user, project=project).role == ProjectRoles.UserRole.ADMIN

    if is_admin:
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        ProjectRoles.objects.filter(project=project, user=user).delete()

    return redirect('project_members', project_id)

@require_POST
@login_required
def task_create(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)
    permission = ProjectRoles.objects.get(user=user, project=project).role != ProjectRoles.UserRole.READONLY

    if permission:
        title = request.POST.get('title')
        task = Task(title=title, project=project)
        task.save()

    return redirect('project_detail', project_id)

@login_required
def completed_tasks(request, project_id):
    username = request.user.username
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project, status=Task.Status.COMPLETED)

    context = {
        'username': username,
        'project': project,
        'tasks': tasks,
        'statuses': Task.Status,
    }

    return render(request, 'completed.html', context)

@login_required
def archieved_tasks(request, project_id):
    username = request.user.username
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project, status=Task.Status.ARCHIVED)

    context = {
        'username': username,
        'project': project,
        'tasks': tasks,
        'statuses': Task.Status,
    }

    return render(request, 'archieved.html', context)

@login_required
def task_detail(request, task_id):
    user = request.user
    username = user.username
    task = Task.objects.get(id=task_id)
    project = task.project
    users = User.objects.filter(projectroles__project=project)
    permission = ProjectRoles.objects.get(user=user, project=project).role != ProjectRoles.UserRole.READONLY

    if request.POST:
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.assignee = User.objects.get(id=request.POST.get('assignee'))
        task.priority = request.POST.get('priority')
        task.save()
        return redirect('project_detail', project.id)

    comments = Comment.objects.filter(task=task)

    context = {
        'username': username,
        'task': task,
        'users': users,
        'permission': permission,
        'priorities': Task.Priority,
        'comments': comments
    }

    return render(request, 'task_detail.html', context)

@login_required
def task_delete(request, task_id):
    user = request.user
    task = Task.objects.get(id=task_id)
    project = task.project
    permission = ProjectRoles.objects.get(user=user, project=project).role != ProjectRoles.UserRole.READONLY

    if permission:
        task.delete()

    return redirect('project_detail', project.id)

@require_POST
@login_required
def task_update_status(request, task_id):
    user = request.user
    task = Task.objects.get(id=task_id)
    project = task.project
    permission = ProjectRoles.objects.get(user=user, project=project).role != ProjectRoles.UserRole.READONLY

    if permission:
        username = request.POST.get('username')
        task = Task.objects.get(id=task_id)
        if 'status' in request.POST:
            task.status = request.POST.get('status')
        else:
            # uncomplete / unarchive
            task.status = Task.Status.INPROGRESS
        task.save()

    return redirect('project_detail', project.id)

@require_POST
@login_required
def comment_create(request, task_id):
    user = request.user
    text = request.POST.get('text')
    task = Task.objects.get(id=task_id)

    comment = Comment(task=task, text=text, author=user)
    comment.save()

    return redirect('task_detail', task_id)

@login_required
def comment_update(request, comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id)

    if user != comment.author:
        return redirect('task_detail', comment.task.id)
    
    if 'text' in request.POST:
        text = request.POST.get('text')
        comment.text = text
        comment.changed = datetime.now()
        comment.edited = True
        comment.save()
        return redirect('task_detail', comment.task.id)
    return render(request, 'comment_edit.html', {
        'username': request.user.username,
        'comment': comment
    })

@require_POST
@login_required
def comment_delete(request, comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id)

    if user != comment.user:
        comment.delete()
    return redirect('task_detail', comment.task.id)
