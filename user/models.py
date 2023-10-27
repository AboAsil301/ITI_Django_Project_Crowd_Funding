# from django.db import models
# import jwt
# from datetime import datetime, timedelta
# from django.conf import settings
# from django.core.validators import RegexValidator
# # Create your models here.
#
# class User(models.Model):
#     # main Data
#     ##me?fields=id,first_name,last_name,birthday,gender,email,picture,link,hometown
#     first_name = models.CharField(max_length=150, blank=False, validators=[
#                                     RegexValidator(r'^[A-Za-z]+$')])
#     last_name = models.CharField(max_length=150, blank=False, validators=[
#                                     RegexValidator(r'^[A-Za-z]+$')])
#     password = models.CharField(max_length=150, blank=False)
#     mobile_phone = models.CharField(blank=False, max_length=11, validators=[
#                                     RegexValidator(r'^01[0-2,5]{1}[0-9]{8}$')])
#     email = models.EmailField(blank=False, unique=True)
#     profile_image = models.ImageField(
#         max_length=255, upload_to="img/%y", null=True, blank=True)
#     # additonal Data
#     country = models.CharField(max_length=30, null=True, blank=True)
#     Birth_date = models.DateField(null=True, blank=True)
#     facebook_profile = models.URLField(max_length=3000, null=True, blank=True)
#     is_verifications = models.BooleanField(default=False)
#     is_authenticated = models.BooleanField(null=True)
#     auth_provider = models.CharField(max_length=255,blank=False,null=False,default='email')
#     last_login=models.DateTimeField(null=True)
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
#
#     @property
#     def token(self):
#         token = jwt.encode({'email': self.email,
#                             'exp': datetime.utcnow()+timedelta(hours=24)},
#                            settings.SECRET_KEY, algorithm='HS256')
#         return token
#


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_phone = models.CharField(max_length=15)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "mobile_phone"]

    def __str__(self):
        return self.email
