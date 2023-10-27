from django.shortcuts import render



# Create your views here.
def register(request):

    return render(request, 'user/registration.html')


def login(request):

    return render(request, "user/login.html")
