from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import ListView, DetailView
from .models import Project

# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'
    login_url = 'account_login'


class ProjectDetailView(
        LoginRequiredMixin,
        DetailView):

    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'
    login_url = 'account_login'


class SearchResultsListView(ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/search_results.html'
    #queryset = Project.objects.filter(project_name__icontains='QLD')

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Project.objects.filter(
            Q(project_name__icontains=query) | Q(
                project_manager__icontains=query) | Q(
                    project_number__icontains=query)
        )
