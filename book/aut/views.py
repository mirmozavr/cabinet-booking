from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    name = request.user.get_username()
    # print('NAME!!!', name)
    if name:
        return render(request, 'index.html', {'name': name})
    return render(request, 'index.html')


def register_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('login')
        user_pass1 = request.POST.get('pass1')
        user_pass2 = request.POST.get('pass2')

        if user_pass1 != user_pass2:
            return render(request, 'register.html', {'error': 'Passwords dont match'})
        print(user_name, user_pass1)
        u = User.objects.create_user(username=user_name, password=user_pass1)
        u.save()

        return redirect('/login_user')

    if request.method == 'GET':
        return render(request, 'register.html')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')


def logout_user(request):
    logout(request)
    return redirect('/')
