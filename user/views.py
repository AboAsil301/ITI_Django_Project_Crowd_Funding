from django.shortcuts import render, redirect, HttpResponse
import re  # Import the 're' module for regular expressions
from django.contrib import messages
from django.core.mail import send_mail  # Add this import

from user.models import User
# Create your views here.
def register(request):
    # print(request)
    # print(request.POST)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']
        mobile_phone = request.POST['mobile_phone']
        profile_image = request.FILES.get('profile_image')

        # Data validation
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        if len(first_name) < 3 or not first_name.isalpha():
            messages.error(request, 'Invalid first name')
            return redirect('register')

        if len(last_name) < 3 or not last_name.isalpha():
            messages.error(request, 'Invalid last name')
            return redirect('register')

        if not email or not email.endswith('.com') or '@' not in email:
            messages.error(request, 'Invalid email')
            return redirect('register')

        if len(password) < 5 or not any(char.isalpha() for char in password) \
                or not any(char.isdigit() for char in password) \
                or not any(char in '@$!%*?&' for char in password):
            messages.error(request, 'Invalid password')
            return redirect('register')

        if password != re_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if not mobile_phone or not re.match(r'^(011|010|012|015)\d{8}$', mobile_phone):
            messages.error(request, 'Invalid mobile phone number')
            return redirect('register')

        if not profile_image or not profile_image.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            messages.error(request, 'Invalid profile image')
            return redirect('register')


        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = password
        user.mobile_phone = mobile_phone
        user.profile_image = profile_image
        # user.save()
        # return redirect('login')

    # return render(request, 'user/registration.html')

        # Generate an activation token
        user.is_active = False  # Set the user as inactive until they activate their email
        user.save()

        # Send an activation email to the user
        activation_token = user.token  # Assuming you have the token property in your User model
        activation_link = f"http://127.0.0.1:7000/user/activate/{activation_token}/"  # Define your activation link

        subject = 'Activate Your Account'
        message = f'Click the following link to activate your account:\n{activation_link}'
        from_email = 'asilmarketo5@gmail.com'  # Change this to your email address
        recipient_list = [email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list)

        # Redirect the user to an activation page or display a message
        return render(request, 'user/activation_instructions.html')

    return render(request, 'user/registration.html')
def login(request):
    return render(request, "user/login.html")

def activate(request, token):
    # You may want to add error handling for expired or invalid tokens
    # For example, check if the token has expired or doesn't match any user in the database

    try:
        user = User.objects.get(token=token)
        user.is_active = True
        user.save()
        return render(request, 'user/activation_success.html')
    except User.DoesNotExist:
        return render(request, 'user/activation_error.html')

def activation_instructions(request):
    return render(request, 'user/activation_instructions.html')
