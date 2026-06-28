from django.db import models
from accounts.models import User

class District(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class MechanicProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_mechanic': True})
    shop_name = models.CharField(max_length=200)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    # Hamne ManyToMany me through model connect kar diya pricing ke liye
    services_offered = models.ManyToManyField(ServiceCategory, through='MechanicServicePrice')

    def __str__(self):
        return self.shop_name

# Ye naya model har service ka alag price save karega
class MechanicServicePrice(models.Model):
    mechanic = models.ForeignKey(MechanicProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Starting price for this service")

    def __str__(self):
        return f"{self.mechanic.shop_name} - {self.service.name} (Rs. {self.base_price})"