from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# User = get_user_model()
# Create your models here.

class Profile(models.Model):
    DEPARTMENT_CHOICES = [
        ('v1', 'Other'),
        ('v2', 'MCA'),
        ('v3', 'MBA'),
        ('v4', 'B-Tech'),
    ]
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    register_no = models.CharField(max_length=150,default="NONE")
    accepted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True, default="This is your bio")
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='profile_pictures/default.png',
        blank=True,
        null=True
    )

    

    

    def __str__(self):
        return self.username