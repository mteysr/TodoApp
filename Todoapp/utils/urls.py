from django.urls import path

from . import views

app_name = "utils"

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('add_todo/', views.add_todo, name='add_todo'),
    path('delete_todo/<int:id>/', views.delete_todo, name='delete_todo'),
    path('complete_todo/<int:todo_id>/', views.complete_todo, name='complete_todo'),
    path('get_todo/<int:todo_id>/', views.get_todo, name='get_todo'),
    # path('update_todo/<int:todo_id>/', views.update_todo, name='update_todo'),
]