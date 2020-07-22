from django.views.generic import ListView, DetailView
from .models import Person
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)


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
