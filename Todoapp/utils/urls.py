from django.urls import path

from . import views

app_name = "utils"

urlpatterns = [
    path("", views.main_page, name="index"),
    path("about/", views.about_page, name="about"),
    
]