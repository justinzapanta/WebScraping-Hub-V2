from django.urls import path
from . import views
from .backend import project_backend, scrapeTool_backend

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('home/', views.home, name='home'),
    path('scan/<str:project_name>', views.scan, name='scan'),

    #project endpoint
    path('api/project/create-project/', project_backend.create_project),

    #scrape api endpoint
    path('api/scrape/delete-step/', scrapeTool_backend.delete_step),
]