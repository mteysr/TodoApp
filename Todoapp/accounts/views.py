from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render



# Create your views here.

def login_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(name, password, email, password)
    return render(request, "login.html")