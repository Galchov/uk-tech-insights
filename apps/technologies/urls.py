# apps/technologies/urls.py

from django.urls import path
from . import views

app_name = 'technologies'

urlpatterns = [
    path('', views.TechnologyListView.as_view(), name='technology_list'),
    path('<int:pk>/', views.TechnologyDetailView.as_view(), name='technology_detail'),
    path('add/', views.TechnologyCreateView.as_view(), name='technology_add'),
    path('<int:pk>/edit/', views.TechnologyUpdateView.as_view(), name='technology_edit'),
    path('<int:pk>/delete/', views.TechnologyDeleteView.as_view(), name='technology_delete'),
]
