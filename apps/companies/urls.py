from django.urls import path
from . import views


app_name = 'companies'

urlpatterns = [
    path('', views.CompanyListView.as_view(), name="company_list"),
    path('add/', views.CompanyAddView.as_view(), name="company_add"),
    path('company/<slug:slug>/', views.CompanyDetailView.as_view(), name="company_detail"),
    path('company/<slug:slug>/edit/', views.CompanyEditView.as_view(), name="company_edit"),
    path('company/<slug:slug>/delete/', views.CompanyDeleteView.as_view(), name="company_delete"),
]
