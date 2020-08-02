from django import forms
from .models import Project, Deliverable
from django.forms.models import formset_factory


class ProjectForm(forms.ModelForm):

    class Meta():
        model = Project
        fields = ['customer', 'project_name', 'project_manager',
                  'project_number']


class DeliverableForm(forms.ModelForm):

    class Meta:
        model = Deliverable
        fields = ('deliverable_name', 'deliverable_description')
