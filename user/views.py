from django.shortcuts import render
from .forms import RegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the registration form data
            # Save user data, send email, etc.
            return render(request, 'registration_success.html')
    else:
        form = RegistrationForm()

    # return render(request, 'user/registration_form.html', {'form': form})
    return render(request, 'user/registration.html', {'form': form})


def login(request):
    # if request.method == 'POST':
    #     form = userLogin(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get("username")
    #         password = form.cleaned_data.get("password")
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         user_info = User.objects.get(username=username)
    #         # user_info2 = user_info.objects.Profile_set.all()
    #         if user_info.is_active == True:
    #             return redirect(index)
    # else:
    #     form = userLogin()
    return render(request, "user/login.html")
