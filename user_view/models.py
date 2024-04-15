from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class User_Subscription(models.Model):
    subcription_id = models.AutoField(primary_key=True)
    user_info = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=200)
    subscription_date = models.DateTimeField(default=timezone.now)


class User_Project(models.Model):
    user_info = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    website_link = models.CharField(max_length=500)
    website_link_title = models.CharField(max_length=35)
    auto_run = models.IntegerField(default=0)
    total_data = models.IntegerField(default=0)
    
