from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Person
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from .forms import PersonForm
from django.urls import reverse_lazy


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    context_object_name = 'person_list'
    template_name = 'persons/person_list.html'
    login_url = 'account_login'


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    context_object_name = 'person'
    template_name = "persons/person_detail.html"
    login_url = 'account_login'


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    context_object_name = 'person'
    template_name = "persons/person_create.html"
    login_url = 'account_login'
    success_url = reverse_lazy('person_list')


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    model = Person
    success_url = reverse_lazy('person_list')
    context_object_name = 'person'
    template_name = "persons/person_delete.html"
    login_url = 'account_login'


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    template_name = "persons/person_update.html"
    login_url = 'account_login'
    form_class = PersonForm
