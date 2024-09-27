from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password



def custom_authenticate(username, password):
    try:
        user = User.objects.get(name=username)
        if check_password(password, user.password):  
            return user
    except User.DoesNotExist:
        return None

def login_view(request):

    if request.method == "POST":
        tmp_name = request.POST.get('username')
        tmp_password = request.POST.get('password')
        user = custom_authenticate(tmp_name, tmp_password)
       
        if user is not None:
            print("Kullanici dogrulandi")

            login(request, user)
            messages.success(request, f"Welcome back, {tmp_name}!")
            
            return redirect('index')  
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password") 
        email = request.POST.get("email")

        if User.objects.filter(name=name).exists():
            messages.error(request, "Username already exists")
            return redirect("accounts:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists") 
            return redirect("accounts:register")


        hashed_password = make_password(password)

        user = User(name=name, email=email, password=hashed_password)
        user.save()

        messages.success(request, f"User {name} successfully registered!")
        return redirect("accounts:login")

    return render(request, "signup.html")