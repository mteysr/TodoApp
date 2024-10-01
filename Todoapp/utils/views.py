from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Todo
from accounts.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required(login_url='accounts:login')
def main_page(request):
    filter_status = request.GET.get('filter', 'all')  # Filtreyi al
    sort_order = request.GET.get('sort', 'nothing')  # Sıralama parametresini al
    todos = Todo.objects.filter(user=request.user)  # Kullanıcıya ait tüm todo'ları al

    # Filtreleme işlemi
    if filter_status == 'completed':
        todos = todos.filter(completed=True)
    elif filter_status == 'active':
        todos = todos.filter(completed=False)

    # Sıralama işlemi
    if sort_order == 'added-date-asc':
        todos = todos.order_by('created_at')  # Varsayılan olarak, 'created_at' alanına göre artan
    elif sort_order == 'added-date-desc':
        todos = todos.order_by('-created_at')  # Azalan sıralama
    elif sort_order == 'due-date-asc':
        todos = todos.order_by('due_date')  # Son tarih artan
    elif sort_order == 'due-date-desc':
        todos = todos.order_by('-due_date')  # Son tarih azalan
    # "nothing" durumu için hiçbir sıralama yapılmayacak
    return render(request, "index.html", {'todos': todos, 'filter_status': filter_status})

@login_required(login_url='accounts:login')
def add_todo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            due_date = data.get('due_date')
            priority = data.get('priority')
            category = data.get('category')

            if not title:
                return JsonResponse({'status': 'error', 'message': 'Title is required'}, status=400)

            # Todo oluştur
            todo = Todo.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                category=category
            )
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            print(f"Error: {str(e)}")  # Hatanın terminale yazılması
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



def get_todos(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(user=request.user)
        todo_list = []
        for todo in todos:
            todo_list.append({
                'title': todo.title,
                'description': todo.description,
                'due_date': todo.due_date.strftime('%Y-%m-%d'),
                'priority': todo.priority,
                'category': todo.category,
                'completed': todo.completed
            })
        return JsonResponse({'todos': todo_list}, status=200)
    

def delete_todo(request, id):
    if request.method == 'DELETE':
        try:
            todo = get_object_or_404(Todo, id=id, user=request.user)
            todo.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def complete_todo(request, todo_id):
    if request.method == 'POST':
        try:
            todo = get_object_or_404(Todo, id=todo_id, user=request.user)
            todo.completed = True
            todo.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def get_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        todo_data = {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'due_date': todo.due_date,
            'priority': todo.priority,
            'category': todo.category,
            'completed': todo.completed,
        }
        return JsonResponse({'status': 'success', 'todo': todo_data})
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Todo not found'}, status=404)