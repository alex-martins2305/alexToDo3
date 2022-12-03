from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from tasks.models  import Task
from django.contrib import auth, messages

def cadastro(request):
    if request.method=='POST':
        nome=request.POST['nome']
        email=request.POST['email']
        senha1=request.POST['password']
        senha2=request.POST['password2']
        if campo_vazio(nome):
            print('O campo nome não pode ficar em branco')
            return redirect('cadastro')
        if campo_vazio(email):
            print('O campo email não pode ficar em branco')
            return redirect('cadastro')
        if senhas_nao_sao_iguais(senha1, senha2):
            messages.error(request, 'As senhas não são iguais')
            print('As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já existe')
            print('Usuário já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha1)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    else:
        return render(request,'usuarios/cadastro.html')
        
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request,'Os campos email e senha não podem ficar em branco')
            return render(request, 'usuarios/login.html')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('tasklist')
        
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'usuarios/login.html')
# Funções de validação:

def campo_vazio(campo):
    return not campo.strip()

def senhas_nao_sao_iguais(senha, senha2):
    return senha != senha2