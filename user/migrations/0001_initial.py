# Generated by Django 4.2.6 on 2023-10-28 01:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[A-Za-z]{3,}$', message='First name must contain at least three letters and only letters.')])),
                ('last_name', models.CharField(max_length=150, validators=[django.core.validators.RegexValidator('^[A-Za-z]{3,}$', message='Last name must contain at least three letters and only letters.')])),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator('[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{3,}$', message='Invalid email format.')])),
                ('password', models.CharField(max_length=128)),
                ('mobile_phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^(011|010|012|015)\\d{8}$', message='Mobile phone must be 11 digits and follow Egyptian mobile number formats (011, 010, 012, or 015)')])),
                ('profile_image', models.ImageField(blank=True, max_length=255, null=True, upload_to='user/images/profile')),
                ('country', models.CharField(blank=True, max_length=30, null=True)),
                ('Birth_date', models.DateField(blank=True, null=True)),
                ('facebook_profile', models.URLField(blank=True, max_length=3000, null=True)),
                ('is_verifications', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('auth_provider', models.CharField(default='email', max_length=255)),
                ('last_login', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
