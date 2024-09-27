from django.contrib import admin
from django.urls import path, include
from utils.views import main_page

urlpatterns = [
    path("", main_page, name="index"),
    path("", include("utils.urls")),
    path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls),
]
