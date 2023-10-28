from django.shortcuts import render, redirect, HttpResponse
import re  # Import the 're' module for regular expressions
from django.contrib import messages
from django.core.mail import send_mail  # Add this import
from django.utils import timezone
from django.conf import settings
import jwt
from datetime import  timedelta
from django.contrib.auth import authenticate, login as auth_login
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
    if request.method == 'POST':
        email = request.POST['email']
        confirm_password = request.POST['password']

        # Check if the user exists and is active
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('login')

        if not user.is_active:
            messages.error(request,
                           'Your account is not activated yet. Please check your email for activation instructions.')
            return redirect('login')

        # Authenticate the user
        # user = authenticate(request, email=email, password=confirm_password)

        if user.password == confirm_password:
            auth_login(request, user)
            user.last_login = timezone.now()
            user.is_verifications = True
            user.save()
            return redirect('profile',user_id=user.id)
            # return HttpResponse(request,"Success")
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
        # if user is not None:
        #     auth_login(request, user)
        #     return redirect('porfile')
        # else:
        #     messages.error(request, 'Invalid email or password')
        #     return redirect('login')

    return render(request, 'user/login.html')


def activation_instructions(request):
    return render(request, 'user/activation_instructions.html')

def activation_success(request):
    return render(request, 'user/activation_success.html')

def activation_error(request):
    return render(request, 'user/activation_error.html')

def activate(request, token):
    try:
        # Decode the token to extract the email
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        email = decoded_token['email']
        print(email)
        # Find the user by their email
        user = User.objects.get(email=email)
        expiration_time = user.created_at + timedelta(hours=24)
        # Check if the token has expired
        if expiration_time and expiration_time < timezone.now():
            # Token has expired, handle this case as needed (e.g., show an error message)
            # return render(request, 'user/activation_error.html', {'error_message': 'Activation link has expired.'})
            messages.error(request, 'Activation link has expired.')
            return redirect('activation_error')

        # Token is valid, activate the user
        user.is_active = True
        user.save()

        # Redirect to a success page
        return redirect('activation_success')
    except jwt.ExpiredSignatureError:
        # Token has expired, handle this case as needed (e.g., show an error message)
        # return render(request, 'user/activation_error.html', {'error_message': 'Activation link has expired.'})
        messages.error(request, 'Activation link has expired.')
        return redirect('activation_error')
    except jwt.DecodeError:
        # Token is invalid, handle this case as needed (e.g., show an error message)
        # return render(request, 'user/activation_error.html', {'error_message': 'Invalid activation link.'})
        messages.error(request, 'Invalid activation link.')
        return redirect('activation_error')
    except User.DoesNotExist:
        # User not found, handle this case as needed (e.g., show an error message)
        # return render(request, 'user/activation_error.html', {'error_message': 'User not found.'})
        messages.error(request, 'User not found.')
        return redirect('activation_error')


def profile(request,user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'user/profile.html/', {'user': user})
