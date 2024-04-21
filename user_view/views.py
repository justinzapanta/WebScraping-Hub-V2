from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import User_Project, User_Project_Process
from bs4 import BeautifulSoup
from .scrape import Scrape, clean, request_data_from_link
import requests
import time
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
        user = User.objects.filter( username=request.POST['email'] )
            
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
    data = {}
    #check is user is authenticated
    if request.user.is_authenticated:
        project = User_Project.objects.filter(
                user_info=request.user,
                project_name=project_name
            )
        data['link'] = project[0].website_link
        request.session['user_project'] = project[0].project_name

        if project:
            process = User_Project_Process.objects.filter(user_project_info=project[0])
            html = request_data_from_link(request, project)
            scrape = Scrape( html=html, project=project[0])
            
            if request.method == 'POST':
                if not process:
                    selection = request.POST['selection']
                    if selection == 'all':
                        scrape.find_tag(request.POST['tag'], save=True)
                    else:
                        scrape.find_with_attribute(
                                request.POST['tag'],
                                selection,
                                request.POST['attribute-name'],
                                save=True
                            )
                else:
                    pass
                process = User_Project_Process.objects.filter(user_project_info=project[0])
                        
            #check if the process have steps then display the result
            _filter = ''
            if process:
                print(len(process))
                process = process[0]
                if process.get_by == '':
                    _filter = scrape.find_tag(process.tag_name)
                else:
                    _filter = scrape.find_with_attribute(
                            process.tag_name,
                            process.get_by,
                            process.attribute_name,
                        )
                


                #i'l remove this later then make it list so that i can display each location
                    data['attribute'] = {'attribute' : process.get_by, 'name' : process.attribute_name}
                data['tag'] = process.tag_name

        _filter = clean(_filter)
        if request.method == 'GET':
            if 'search' in request.GET:
                temp_list = []

                for datas in _filter:
                    for value in datas:
                        if request.GET['search'] in str(value):
                            temp_list.append(datas)
                            break
                _filter = temp_list

        data['results'] = _filter
        return render(request, 'user_view/home_page/webscrape.html', data)
    return redirect('home')