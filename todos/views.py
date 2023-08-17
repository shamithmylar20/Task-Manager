from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .models import Todo


# Create your views here.
def list_todo_items(request):
    user = request.user
    context ={'todo_list' : Todo.objects.filter(user=user), 'name' : user.first_name}
    return render(request, 'todos/todo_list.html', context)

def insert_todo_item(request):    
    if request.user.is_authenticated:
        user = request.user
        todo = Todo(content = request.POST['content'], user=user)
        todo.save()
        return redirect('/todos/list/')
    else:
        return redirect('/login/')

def delete_todo_item(request, todo_id):
    todo_to_delete = Todo.objects.get(id=todo_id)
    todo_to_delete.delete()
    return redirect('/todos/list/')