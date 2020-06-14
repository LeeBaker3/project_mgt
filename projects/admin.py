from django.contrib import admin
from .models import Project, Deliverable

# Register your models here.


class DeliverableInline(admin.TabularInline):
    model = Deliverable


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        DeliverableInline
    ]
    list_display = ('project_number', 'project_name', 'project_manager',)


admin.site.register(Project, ProjectAdmin)
