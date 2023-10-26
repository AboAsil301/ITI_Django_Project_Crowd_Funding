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

    return render(request, 'user/registration_form.html', {'form': form})
