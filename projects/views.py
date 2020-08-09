from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Project, Deliverable
from .forms import (ProjectForm, DeliverableForm)
from django.urls import reverse_lazy


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


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    context_object_name = 'project'
    template_name = "projects/project_create.html"
    login_url = 'account_login'
    success_url = reverse_lazy('project_list')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = "projects/project_update.html"
    login_url = 'account_login'
    form_class = ProjectForm


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project_delete.html"
    success_url = reverse_lazy('project_list')
    context_object_name = 'project'
    login_url = 'account_login'


class ProjectDeliverableDetailView(
        LoginRequiredMixin,
        DetailView):
    model = Deliverable
    context_object_name = 'deliverable'
    template_name = 'projects/deliverable_detail.html'
    login_url = 'account_login'


class ProjectDeliverableCreateView(LoginRequiredMixin, CreateView):
    model = Deliverable
    form_class = DeliverableForm
    context_object_name = 'deliverable'
    template_name = "projects/deliverable_create.html"
    login_url = 'account_login'

    def form_valid(self, form):
        self.project = Project.objects.get(
            id=self.kwargs['project_id'])
        form.instance.project = self.project
        self.success_url = self.project.get_absolute_url()
        return super(ProjectDeliverableCreateView, self).form_valid(form)


class ProjectDeliverableUpdateView(LoginRequiredMixin, UpdateView):
    model = Deliverable
    template_name = "projects/deliverable_update.html"
    login_url = 'account_login'
    form_class = DeliverableForm
    login_url = 'account_login'

    def form_valid(self, form):
        self.project = self.object.project
        self.success_url = self.project.get_absolute_url()
        return super().form_valid(form)


class ProjectDeliverableDeleteView(LoginRequiredMixin, DeleteView):
    model = Deliverable
    template_name = "projects/deliverable_delete.html"
    login_url = 'account_login'
    form_class = DeliverableForm
    login_url = 'account_login'

    def get_success_url(self):
        self.project = self.object.project
        return self.project.get_absolute_url()


class SearchResultsListView(ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/search_results.html'
    # queryset = Project.objects.filter(project_name__icontains='QLD')

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Project.objects.filter(
            Q(project_name__icontains=query) | Q(
                project_manager__icontains=query) | Q(
                    project_number__icontains=query)
        )


# class DeliverableCreateView(LoginRequiredMixin, CreateView):
#     model = Deliverable
#     form_class = DeliverableForm
#     template_name = "deliverables/deliverable_create.html"
