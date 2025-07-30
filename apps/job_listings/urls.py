from django.urls import path

from . import views


app_name = 'job_listings'

urlpatterns = [
    path('', views.JobsPostListView.as_view(), name="jobs_list"),
    path('add/', views.JobPostAddView.as_view(), name="add_job"),
    path('<slug:slug>/', views.JobPostDetailView.as_view(), name="job_detail"),
    path('<slug:slug>/edit/', views.JobPostUpdateView.as_view(), name="job_edit"),
    path('<slug:slug>/toggle-status/', views.JobPostToggleStatusView.as_view(), name="job_toggle_status"),
    path('<slug:slug>/apply/', views.JobApplicationCreateView.as_view(), name="apply"),
]
