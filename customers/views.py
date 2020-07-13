from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Customer

# Create your views here.


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    context_object_name = 'customer_list'
    template_name = 'customers/customer_list.html'
    login_url = 'account_login'


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'customers/customer_detail.html'
    login_url = 'account_login'
