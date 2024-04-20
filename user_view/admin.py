from django.contrib import admin
from .models import User_Subscription, User_Project, User_Project_Process

# Register your models here.
admin.site.register([
    User_Subscription,
    User_Project,
    User_Project_Process,
])