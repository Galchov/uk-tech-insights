from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import Request
from django.contrib.auth.decorators import login_required


# TODO: To be implemented
# @login_required   
def dashboard_view(request: Request) -> HttpResponse:
    return render(request, 'users/dashboard.html')


def profile_details_view(request: Request, pk: int) -> HttpResponse:
    return render(request, 'users/profile_details.html')


def profile_edit_view(request: Request, pk: int) -> HttpResponse:
    return render(request, 'users/profile_edit.html')
