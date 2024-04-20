from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from ..models import User_Project_Process, User_Project
import json

@csrf_exempt
def delete_step(request):
    if request.method == 'POST':
        project = User_Project.objects.get(
                user_info=request.user, 
                project_name=request.session['user_project']
            )
        
        process = User_Project_Process.objects.filter(user_project_info=project)
        process[len(process)-1].delete()
    return JsonResponse({'message' : 'Success'}, status=200)