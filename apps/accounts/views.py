from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import Request


def sign_in_view(request: Request) -> HttpResponse:
    return render(request, 'accounts/sign-in-page.html', {'hide_navbar': True})
