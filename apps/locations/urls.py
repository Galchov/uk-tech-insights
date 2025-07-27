from django.urls import path

from . import views


app_name = 'locations'

urlpatterns = [
    path('locations/', views.LocationListView.as_view(), name="location_list"),
    path('locations/add/', views.LocationCreateView.as_view(), name="location_add"),
    path('locations/<int:city_id>/', views.LocationEditView.as_view(), name="location_edit"),
    path('delete/<int:pk>/', views.LocationDeleteView.as_view(), name='location_delete'),
]
