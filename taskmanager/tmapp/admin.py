from django.contrib import admin
from .models import Project, ProjectRoles, Task, Comment

admin.site.register(Project)
admin.site.register(ProjectRoles)
admin.site.register(Task)
admin.site.register(Comment)
