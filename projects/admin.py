from django.contrib import admin
from .models import Project

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_number', 'project_name', 'project_manager',)


admin.site.register(Project, ProjectAdmin)
