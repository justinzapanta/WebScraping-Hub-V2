from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'user_view/index.html')


def home(request):
    return render(request, 'user_view/home_page/home_page.html')



def sign_in(request):
    data = {'notif' : ''}

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = authenticate(
            username=request.POST['email'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('home') 
        
        data['notif'] = 'Invalid Email or Password'

    return render(request, 'user_view/authentication/sign_in.html', data)



def sign_up(request):
    data = {'notif' : ''}

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        user = User.objects.filter(
            username=request.POST['email']
        )
            
        if not user:
            user = User.objects.create_user(
                username=request.POST['email'],
                password=request.POST['password'],
                email=request.POST['email']
            )
            user.save()
            return redirect('sign-in')

        data['notif'] = 'Email Already Exists'
    return render(request, 'user_view/authentication/sign_up.html', data)



def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')
    

def scan(request):
    return render(request, 'user_view/home_page/webscrape.html')