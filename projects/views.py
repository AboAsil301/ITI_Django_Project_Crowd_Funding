from django.shortcuts import render, redirect
from projects.models import Projects,Pictures,Tags,Categories,Rates
from projects.forms import CategoryForm, ProjectForm
from user.models import User
from django.db.models import Q ,Avg

# from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request, user_id):
  user = User.objects.get(id=user_id)
  projects = Projects.objects.all()
  return render(request, 'projects/index.html', context={"projects":projects, "user": user})


# @login_required
def create_project(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = user  # Set the project owner as the currently logged-in user
            project.save()

            # Process and associate uploaded images
            for image in request.FILES.getlist('images'):
                pic = Pictures(image=image, project=project)
                pic.save()

            # Process and split the tags
            tags = request.POST.get('tags')  # Get the tags field from the POST data
           # print(tags)

            tag_list = [tag.strip() for tag in tags.split(',')]  # Split tags by comma
           # print(tag_list)
            for tag in tag_list:
                tag_obj = Tags(tag=tag, project=project)
                tag_obj.save()

            # Associate the project with the user

            # Redirect to the created project
            return redirect('profile', user_id)

    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {'form': form, 'user': user})

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



def details(request, project_id):
    project = Projects.objects.get(id=project_id)
    # Get all images related to the project
    images = Pictures.objects.filter(project=project)

    return render(request, 'projects/project-details.html', {'project': project, 'images': images})




def homepage(request):

    # Retrieve highest-rated projects
    highest_rated_projects = Projects.objects.order_by('-rate')[:5]

    # Retrieve latest projects
    latest_projects = Projects.objects.order_by('-created_at')[:5]

    # Retrieve latest featured projects
    featured_projects = Projects.objects.order_by('-selected_at_by_admin')[:5]

    # Retrieve all project categories
    categories = Categories.objects.all()

    # Retrieve all projects images
    images = Pictures.objects.all()

    context = {
        'highest_rated_projects': highest_rated_projects,
        'latest_projects': latest_projects,
        'featured_projects': featured_projects,
        'categories': categories,
        'images': images,

    }
    return render(request, 'projects/homepage.html', context)

def search(request):
    query = request.GET.get('query')
    # Perform a search based on the query (project title or tag)
    results = Projects.objects.filter(Q(title__icontains=query) | Q(tags__tag__icontains=query), is_running=True)
    context = {'query': query, 'results': results}
    return render(request, 'projects/search_results.html', context)


def handle_rating_submission(request, project_id, rating):
    # Assuming you have obtained the project and rating data
    project = Projects.objects.get(id=project_id)
    user = request.user  # Assuming you have a user object
    # Create a new Rates object and save it
    rate = Rates(rate=rating, project=project, user=user)
    rate.save()

    # Update the project's average rating if needed
    # For example, calculate the new average rating based on all ratings for this project
    project.rate = calculate_average_rating(project)
    project.save()

    # Handle the rest of your response or redirect as needed


def calculate_average_rating(project):
    # Calculate the average rating for a specific project
    average_rating = Rates.objects.filter(project=project).aggregate(Avg('rate'))['rate__avg']

    # Check if the result is not None (i.e., there are ratings for the project)
    if average_rating is not None:
        return round(average_rating, 2)  # You can round the average to 2 decimal places
    else:
        return 0  # If there are no ratings, return a default value
