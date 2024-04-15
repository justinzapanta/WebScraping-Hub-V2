from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import User_Project
from bs4 import BeautifulSoup
import requests
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'user_view/index.html')


def home(request):
    if request.user.is_authenticated:
        user_projects = User_Project.objects.filter(user_info=request.user)
        return render(request, 'user_view/home_page/home_page.html', {'projects' : user_projects})
    return redirect('index')



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
    

def scan(request, project_name):
    project = User_Project.objects.filter(
        user_info=request.user,
        project_name=project_name
    )
    
    if project:
        data = {}
        data['link'] = project[0].website_link

        if 'project' not in request.session or request.session['project']['project_name'] != project_name:
            website_html = requests.get(project[0].website_link).text
            request.session['project'] = {
                'project_name' : project_name,
                'html' : website_html
            }

        if request.method == 'POST':
            if request.POST['get']:
                html = request.session['project']['html']
                soup = BeautifulSoup(html, 'lxml')
                filter_ = soup.find_all(request.POST['tag'])
                
                data['tag'] = request.POST['tag']
                data['results'] = filter_
        
        return render(request, 'user_view/home_page/webscrape.html', data)
    return redirect('home')
