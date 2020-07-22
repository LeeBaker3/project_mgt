# person/urls.py
from django.urls import path
from .views import PersonListView, PersonDetailView

urlpatterns = [
    path('', PersonListView.as_view(), name='person_list'),
    path('<uuid:pk>', PersonDetailView.as_view(), name='person_detail'),
]
