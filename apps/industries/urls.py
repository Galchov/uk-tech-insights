from django.urls import path

from . import views


app_name = 'industries'


urlpatterns = [
    path('', views.IndustryListView.as_view(), name='industry_list'),
    path('add/', views.IndustryCreateView.as_view(), name='industry_add'),
    path('<int:pk>/edit/', views.IndustryUpdateView.as_view(), name='industry_edit'),
    path('<int:pk>/delete/', views.IndustryDeleteView.as_view(), name='industry_delete'),
]