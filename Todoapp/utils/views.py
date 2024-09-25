from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.

def main_page(request):
    return render(request, "index.html")

def about_page(request):
    return render(request, "utils/about.html")