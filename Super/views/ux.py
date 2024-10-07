from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Super.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views import View

class RegisterView(View):
    def get(self, request):
        context = {'title': 'Registro de Usuario', 'form': UserCreationForm()}
        return render(request, 'ux/register.html', context)

    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('Super:home')
            except IntegrityError:
                context = {'title': 'Registro de Usuario', 
                           'form': UserCreationForm(request.POST), 
                           'error': 'Usuario ya existe'}
                return render(request, 'ux/register.html', context)
        else:
            context = {'title': 'Registro de Usuario', 
                       'form': UserCreationForm(request.POST), 
                       'error': 'Las contraseñas no coinciden'}
            return render(request, 'ux/register.html', context)

class LoginView(View):
    def get(self, request):
        context = {'title': 'Iniciar Sesión', 'form': AuthenticationForm()}
        return render(request, 'ux/login.html', context)

    def post(self, request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {'title': 'Iniciar Sesión', 
                       'form': AuthenticationForm(), 
                       'error': 'Usuario o contraseña incorrectos'}
            return render(request, 'ux/login.html', context)
        else:
            login(request, user)
            return redirect('Super:home')

@login_required
def logoutview(request):
    logout(request)
    return redirect('Super:login')








