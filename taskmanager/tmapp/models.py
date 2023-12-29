from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class ProjectRoles(models.Model):

    class UserRole(models.TextChoices):
        ADMIN = 'ADM', _('Admin')
        RW = 'RW', _('Read-Write')
        READONLY = 'RO', _('Read-only')

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=3, choices=UserRole.choices, default=UserRole.READONLY)


class Task(models.Model):

    class Priority(models.TextChoices):
        LOW = 'L', _('Low')
        MEDIUM = 'M', _('Medium')
        HIGH = 'H', _('High')
        NOT_SET = 'N', _('Not set')

    class Status(models.TextChoices):
        INPROGRESS = 'IP', _('In Progress')
        COMPLETED = 'C', _('Completed')
        ARCHIVED = 'A', _('Archived')

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.INPROGRESS)
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.CharField(
        max_length=1, choices=Priority.choices, default=Priority.NOT_SET)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    changed = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
