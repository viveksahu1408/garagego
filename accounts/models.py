from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Role segregation ke liye Boolean fields
    is_customer = models.BooleanField(default=False)
    is_mechanic = models.BooleanField(default=False)
    is_admin_staff = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({'Mechanic' if self.is_mechanic else 'Customer' if self.is_customer else 'Admin'})"