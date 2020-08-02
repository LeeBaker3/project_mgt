# projects/urls.py

from django.urls import path
from .views import (ProjectListView, ProjectDetailView,
                    SearchResultsListView, ProjectCreateView,
                    ProjectUpdateView, ProjectDeleteView,
                    ProjectDeliverableUpdateView, ProjectDeliverableCreateView,
                    ProjectDeliverableDeleteView,)


urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('<uuid:pk>', ProjectDetailView.as_view(), name='project_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('update/<uuid:pk>', ProjectUpdateView.as_view(), name='project_update'),
    path('delete/<uuid:pk>', ProjectDeleteView.as_view(), name='project_delete'),
    path('deliverable/update/<int:pk>', ProjectDeliverableUpdateView.as_view(),
         name='project_deliverable_update'),
    path('deliverable/create/<uuid:project_id>', ProjectDeliverableCreateView.as_view(),
         name='project_deliverable_create'),
    path('deliverable/delete/<int:pk>', ProjectDeliverableDeleteView.as_view(),
         name='project_deliverable_delete'),
]
