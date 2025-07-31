from django.urls import path
from . import views


app_name = 'common'

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('public-api/', views.PublicAPIPageView.as_view(), name="public_api"),
    path('<str:model>/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
]
