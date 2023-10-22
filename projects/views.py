from django.shortcuts import render
from projects.models import Projects

# Create your views here.
def index(request):
  projects = Projects.objects.all()
  return render(request, 'projects/index.html', context={"projects":projects})
