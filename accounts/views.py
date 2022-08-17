from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato
from contatos.views import index

# Create your views here.


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    
    user = auth.authenticate(request, username=usuario, password = senha)
    
    if not user:
        messages.error(request, 'Usuario e/ou senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Você Logou com sucesso')
        return redirect('index')
    

def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    
    if not nome or not sobrenome or not email \
        or not usuario or not senha or not senha2:
        messages.info(request, 'Preencha todos os campos')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail Invalido')
        return render(request, 'accounts/register.html')
    
    if len(senha) < 8:
        messages.info(request, 'Senha precisa ser maior que 8 caracteres')
        return render(request, 'accounts/register.html')
    if len(usuario) < 6:
        messages.info(request, 'Usuario precisa ter mais que 6 caracteres')
        return render(request, 'accounts/register.html')
    if senha != senha2:
        messages.info(request, 'As senhas precisam ser iguais')
        return render(request, 'accounts/register.html')
    if User.objects.filter(username=usuario).exists():
        messages.info(request, 'Usuario já existe')
        return render(request, 'accounts/register.html')
    if User.objects.filter(email=email).exists():
        messages.info(request, 'E-mail já cadastrado')
        return render(request, 'accounts/register.html')
    
    messages.success(request, 'Registrado com Sucesso!')
    
    user=User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('index')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)
    
    
    if not form.is_valid():
        messages.error(request, 'ERRO AO ENVIAR FORMULARIO')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
    
    descricao = request.POST.get('descricao')
    
    if len(descricao) < 7:
        messages.error(request, 'Descrição precisa ser Maior')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
    
    form.save()
    messages.success(request, 'Contato Gravado com sucesso')
    return redirect('dashboard')
        