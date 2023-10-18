from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True) 


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users'  # Custom related name for groups
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users'  # Custom related name for user_permissions
    )


    def __str__(self):
        return self.username




