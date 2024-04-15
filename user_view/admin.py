from django.contrib import admin
from .models import User_Subscription, User_Project

# Register your models here.
admin.site.register([
    User_Subscription,
    User_Project
])