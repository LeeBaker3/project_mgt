# person/urls.py
from django.urls import path
from .views import (PersonListView, PersonDetailView,
                    PersonCreateView, PersonDeleteView, PersonUpdateView)

urlpatterns = [
    path('', PersonListView.as_view(), name='person_list'),
    path('<uuid:pk>', PersonDetailView.as_view(), name='person_detail'),
    path('create/', PersonCreateView.as_view(), name='person_create'),
    path('delete/<uuid:pk>', PersonDeleteView.as_view(), name='person_delete'),
    path('update/<uuid:pk>', PersonUpdateView.as_view(), name='person_update'),
]
