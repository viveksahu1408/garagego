from django.db import models
from accounts.models import User
from services.models import District

class CarListing(models.Model):
    CONDITION_CHOICES = [
        ('Excellent', 'Excellent (Ekdum Nayi Jaisi)'),
        ('Good', 'Good (Achhi Condition)'),
        ('Fair', 'Fair (Theek Thaak)'),
    ]

    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('Electric', 'Electric'),
    ]

    # 👤 Seller Details
# models.py ke andar CarListing model me:
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)    
    seller_name = models.CharField(max_length=100, default="Unknown Seller")
    seller_phone = models.CharField(max_length=15, default="")
    
    # 🚗 Car Specifications (Jo pehle chahiye the)
    brand = models.CharField(max_length=50)
    car_name = models.CharField(max_length=100)
    model_year = models.IntegerField()
    kms_driven = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    expected_price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(District, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    
    # 📄 Documents Verification Checklist
    has_rc_card = models.BooleanField(default=False)
    has_noc = models.BooleanField(default=False)
    insurance_status = models.CharField(max_length=100, default="Expired")

    # 📸 Multiple Car Photos (4 Angles)
    image_front = models.ImageField(upload_to='car_bazaar_pics/', blank=True, null=True)
    image_back = models.ImageField(upload_to='car_bazaar_pics/', blank=True, null=True)
    image_interior = models.ImageField(upload_to='car_bazaar_pics/', blank=True, null=True)
    image_dashboard = models.ImageField(upload_to='car_bazaar_pics/', blank=True, null=True)
    
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.car_name} ({self.model_year})"