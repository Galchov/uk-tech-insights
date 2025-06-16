from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import Request


def home_page_view(request: Request) -> HttpResponse:
    return render(request, 'common/home-page.html')
