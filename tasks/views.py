from django.shortcuts import redirect, render, get_object_or_404, redirect
from .models import Task
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from datetime import date
from usuarios.views import campo_vazio
from django.http import HttpResponse

task_global=''

def tasklist(request):
    try:
        if request.user.is_authenticated:
            id = request.user.id

            Tasks_atrasadas1=Task.objects.filter(ends_at__lt=date.today(), pessoa=id).values().order_by('-created_at') 
            Tasks_atrasadas=Tasks_atrasadas1.filter(etapas='não iniciada')|Tasks_atrasadas1.filter(etapas='iniciada')

            TasksDoDia1=Task.objects.filter(ends_at__exact=date.today(), pessoa=id ).values().order_by('-created_at')
            TasksDoDia=TasksDoDia1.filter(etapas='iniciada')|TasksDoDia1.filter(etapas='não iniciada')
            
            Tasks_futuras1=Task.objects.filter(ends_at__gt=date.today(), pessoa=id ).values().order_by('-created_at')
            Tasks_futuras=Tasks_futuras1.filter(etapas='não iniciada')|Tasks_futuras1.filter(etapas='iniciada')

            return render(request, 'tasks/list.html',{'Tasks_atrasadas':Tasks_atrasadas, 'TasksDoDia':TasksDoDia, 'tasks_futuras':Tasks_futuras})  
        else:
            return render(request, 'usuarios/login.html')
    except ValueError:
        print('Deu ruim')
        return render(request, 'usuarios/login.html')

def tasksvencidas(request):
    if request.user.is_authenticated:
        id = request.user.id
        Tasks_atrasadas1=Task.objects.filter(ends_at__lt=date.today(), pessoa=id).values().order_by('-created_at') 
        Tasks_atrasadas=Tasks_atrasadas1.filter(etapas='não iniciada')|Tasks_atrasadas1.filter(etapas='iniciada')
        return render(request, 'tasks/tasksvencidas.html',{'tasks_atrasadas':Tasks_atrasadas})   
    else:
        return render(request, 'usuarios/login.html')

def tasksDoDia(request):
    if request.user.is_authenticated:
        id = request.user.id
        TasksDoDia1=Task.objects.filter(ends_at__exact=date.today(), pessoa=id).values().order_by('-created_at') 
        TasksDoDia=TasksDoDia1.filter(etapas='iniciada')|TasksDoDia1.filter(etapas='não iniciada')
        return render(request, 'tasks/tasksDoDia.html',{'TasksDoDia':TasksDoDia})   
    else:
        return render(request, 'usuarios/login.html')

def tasksFuturas(request):
    if request.user.is_authenticated:
        id = request.user.id
        TasksFuturas1=Task.objects.filter(ends_at__gt=date.today(), pessoa=id).values().order_by('-created_at') 
        TasksFuturas=TasksFuturas1.filter(etapas='não iniciada')|TasksFuturas1.filter(etapas='iniciada')
        return render(request, 'tasks/tasksFuturas.html',{'TasksFuturas':TasksFuturas})   
    else:
        return render(request, 'usuarios/login.html')

def tasksEncerradas(request):
    if request.user.is_authenticated:
        id = request.user.id
        TasksEncerradas=Task.objects.filter(etapas='finalizada', pessoa=id).values().order_by('concluida_at') 
        return render(request, 'tasks/tasksEncerradas.html',{'tasksEncerradas':TasksEncerradas})   
    else:
        return render(request, 'usuarios/login.html') 

def tasksJustificadas(request):
    if request.user.is_authenticated:
        id = request.user.id
        tasksJustificadas=Task.objects.filter(etapas='justificada', pessoa=id).values().order_by('concluida_at') 
        return render(request, 'tasks/tasksJustificadas.html',{'tasksJustificadas':tasksJustificadas})   
    else:
        return render(request, 'usuarios/login.html')

def taskview(request,id):
    global task_global
    task_global=get_object_or_404(Task, pk=id)
    #diasAtraso1=abs((task_global.concluida_at-task_global.ends_at).days)
    #print(diasAtraso1)
    #if diasAtraso1>0:
    #    diasAtraso=diasAtraso1
    #print(diasAtraso)
    return render(request, 'tasks/task.html',{'task':task_global})

def starttask(request):
    try:
        task_global.etapas='iniciada'
        task_global.start_at=date.today()
        task_global.save()
        return render(request, 'tasks/task.html',{'task':task_global})   
    except ValueError:
         return redirect('task') 

def justtask(request):
    try:
        task_global.etapas='justificada'
        task_global.concluida_at=date.today()
        diasAtraso=(task_global.concluida_at-task_global.ends_at).days
        print(diasAtraso)
        task_global.save()
        return render(request, 'tasks/task.html',{'task':task_global})
    except ValueError:
        return redirect('task')

def stoptask(request):
    try:
        task_global.etapas='finalizada'
        task_global.concluida_at=date.today()
        diasAtraso=task_global.concluida_at-task_global.start_at
        task_global.save()
        return render(request, 'tasks/task.html',{'task':task_global})
    except ValueError:
        return redirect('task')
    
def newtask(request):
    try:
        if request.method=='POST':
            titulo=request.POST['titulo']
            descricao=request.POST['descricao']
            ends_at=request.POST['ends_at']
            pessoa=get_object_or_404(User, pk=request.user.id)
            if campo_vazio(titulo):
                return redirect('newtask')
            if campo_vazio(descricao):
                return redirect('newtask')
            if campo_vazio(ends_at):
                return redirect('newtask')
            task = Task.objects.create(pessoa=pessoa, titulo=titulo, etapas='não iniciada', status='ativa', descricao=descricao, ends_at=ends_at, concluida_at='9999-12-31')
            task.save()
            messages.success(request, 'Nova tarefa criada!')
            return redirect('/')
        else:    
            return render(request, 'tasks/newtask1.html')
    except ValueError:
        return redirect ('newtask')

def salvaObs(request): 
    if request.method == 'POST':
        obs=request.POST['obs']
        task_global.obs=obs
        task_global.save()
    else:
        print('Não salvou')
    return render(request, 'tasks/task.html',{'task':task_global})

def buscar(request):
    lista_tasks= Task.objects.all().order_by('-created_at')

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            lista_tasks = lista_tasks.filter(titulo__icontains=nome_a_buscar)

    return render(request, 'tasks/buscar.html', {"tasks":lista_tasks})

def funcSalvaObs(request):
    if request.method == 'POST':
        obs=request.POST['obs']
        task_global.obs=obs
        task_global.save()
    elif request.method=='GET':
        obs=request.GET['obs']
        print(obs)
    else:
        print('Não salvou')