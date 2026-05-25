from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser

def index(request):
    return render(request, 'operations/index.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'username is already taken')
            return redirect('/operations/signup/')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists, kindly login')
            return redirect('/operations/login/')
        user = CustomUser.objects.create_user(
            email=email,
            username=username,  
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password
        )

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('/operations/login/')

    return render(request, 'operations/signup.html')



def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except user.DoesNotExist:
            messages.error(request, 'Invalid Email')
            return redirect('/login/')


        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/operations/')

    return render(request, 'operations/login.html')

def user_logout(request):
    logout(request)
    return redirect('/operations/')

