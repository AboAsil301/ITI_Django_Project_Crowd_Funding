from django.db import models
import jwt
from datetime import datetime , timedelta
from django.utils import timezone  # Import timezone from Django
from django.conf import settings
from django.core.validators import RegexValidator
# Create your models here.

class User(models.Model):
    # main Data
    first_name = models.CharField(
        max_length=20,
        blank=False,
        validators=[
            RegexValidator(
                r'^[A-Za-z]{3,}$',
                message='First name must contain at least three letters and only letters.',
            ),
        ]
    )

    last_name = models.CharField(
        max_length=150,
        blank=False,
        validators=[
            RegexValidator(
                r'^[A-Za-z]{3,}$',
                message='Last name must contain at least three letters and only letters.',
            ),
        ]
    )

    email = models.EmailField(
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{3,}$',
                message='Invalid email format.',
            ),
        ]
    )

    password = models.CharField(
        max_length=128,
        blank=False
    )

    mobile_phone = models.CharField(
        max_length=11,
        blank=False,
        validators=[
            RegexValidator(
                r'^(011|010|012|015)\d{8}$',
                message='Mobile phone must be 11 digits and follow Egyptian mobile number formats (011, 010, 012, or 015)',
            ),
        ]
    )

    profile_image = models.ImageField(
        max_length=255,
        upload_to="user/images/profile",
        null=True,
        blank=True
    )

    # Additional Data
    country = models.CharField(max_length=30, null=True, blank=True , default='Egypt')
    Birth_date = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(max_length=3000, null=True, blank=True)
    is_verifications = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default='email')
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def token(self):
        expiration_time = timezone.now() + timedelta(hours=24)
        token = jwt.encode({'email': self.email, 'exp': expiration_time},
                           settings.SECRET_KEY, algorithm='HS256')
        return token
