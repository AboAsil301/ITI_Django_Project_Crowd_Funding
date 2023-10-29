from django.shortcuts import render, redirect
from projects.models import Projects
from projects.forms import CategoryForm, ProjectForm
from user.models import User
# from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
  projects = Projects.objects.all()
  return render(request, 'projects/index.html', context={"projects":projects})


# @login_required
def create_project(request, user_id):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        user = User.objects.get(id=user_id)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = user # Set the project owner as the currently logged-in user
            project.save()
            return redirect('projects.index')
    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {'form': form})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects.index')
    else:
        form = CategoryForm()

    return render(request, 'projects/create_category.html', {'form': form})

def index(request):
    projects = Projects.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})
