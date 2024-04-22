from bs4 import BeautifulSoup
from .models import User_Project_Process
import requests

def request_data_from_link(request, project):
    if 'project' not in request.session or request.session['project']['project_name'] != project[0].project_name:
        website_html = requests.get(project[0].website_link).text

        request.session['project'] = {
                'project_name' : project[0].project_name,
                'html' : website_html
            }
    return request.session['project']['html']


def clean(data):
    result = []
    
    temp_list = []
    for values in data:
        if len(values) >= 2:
            for value in values:
                if value != '\n':
                    temp_list.append(value)

            result.append(temp_list)
            temp_list = []
        else:
            result.append([value])
    return result
    

class Scrape():
    def __init__(self, html, project):
        self.project = project
        self.bs4 = BeautifulSoup(html, 'lxml') 
    

    def find_tag(self, tag, selection, save=False):
        if save:
            filter_process = User_Project_Process(
                    user_project_info=self.project,
                    tag_name=tag,
                    get_by=selection
                )
            filter_process.save()
        return self.bs4.find_all(tag)


    def find_with_attribute(self, tag, attribute, name, save=False):
        if save:
            filter_process = User_Project_Process(
                    user_project_info=self.project,
                    tag_name=tag,
                    get_by=attribute,
                    attribute_name=name
                )
            filter_process.save()

        if attribute == 'id':
            return self.bs4.find(tag, id=name)
        else:
            return self.bs4.find_all(tag, class_=name)
    

    def get_process(self):
        return User_Project_Process.objects.filter(user_project_info=self.project)
    

    def save_process(self, tag):
        pass

