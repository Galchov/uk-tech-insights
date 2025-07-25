from django.urls import path
from . import views


app_name = 'companies'

urlpatterns = [
    path('', views.CompanyListView.as_view(), name="company_list"),
    path('add-company/', views.CompanyAddView.as_view(), name="company_add"),
    path('company/<slug:slug>/', views.CompanyDetailView.as_view(), name="company_detail"),
    path('company/<slug:slug>/edit/', views.CompanyEditView.as_view(), name="company_edit"),
    path('company/<slug:slug>/delete/', views.CompanyDeleteView.as_view(), name="company_delete"),

    path('add-location/', views.LocationAddView.as_view(), name="location_add"),
    path('locations/', views.LocationListView.as_view(), name="location_list"),
    path('locations/<int:pk>/', views.LocationEditView.as_view(), name="location_edit_detail"),
    path('locations/<int:pk>/delete/', views.LocationDeleteView.as_view(), name="location_confirm_delete"),
]
