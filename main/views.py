from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Сама проверка, есть ли пользователь в БД

        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            error_message = 'Неверное имя пользователя или пароль'

    return render(request, 'main/log_in.html')


def reg_page(request):
    if request.method == 'POST':
        new_user = User.objects.create_user(request.POST.get("name"), request.POST.get("email"), request.POST.get("password"))
        new_user.save()

    return render(request, 'main/register.html')


def log_out(request):
    logout(request)
    return redirect('/')

