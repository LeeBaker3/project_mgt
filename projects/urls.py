# projects/urls.py
from django.urls import path
from .views import ProjectListView, ProjectDetailView, SearchResultsListView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('<uuid:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
]
