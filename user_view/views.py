from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'user_view/index.html')


def sign_in(request):
    return render(request, 'user_view/authentication/sign_in.html')