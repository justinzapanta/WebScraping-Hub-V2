from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import User_Project
import json

@csrf_exempt
def create_project(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            project = User_Project.objects.filter(
                user_info=request.user,
                project_name=data['project-name']
            )
            
            link_title = data['website-url']
            if not project:
                if len(str(data['website-url'])) > 29:
                    link_title = data['website-url'][0:29]

                new_project = User_Project(
                    user_info=request.user,
                    project_name=data['project-name'],
                    website_link=data['website-url'],
                    website_link_title=link_title
                )
                new_project.save()
                return JsonResponse({'message' : 'success'}, status=200)
            
            return JsonResponse({'message' : 'Project Name already exists'}, status=409)
        return JsonResponse({'message' : 'Something Wrong'}, status=404)
    return JsonResponse({'message' : 'Please Login'}, status=409)
    