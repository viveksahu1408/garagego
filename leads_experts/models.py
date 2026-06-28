from django.db import models
from accounts.models import User
from services.models import MechanicProfile

class CallLog(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    mechanic = models.ForeignKey(MechanicProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Call to {self.mechanic.shop_name} at {self.timestamp}"

class ExpertInquiry(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    query_details = models.TextField(help_text="e.g., 5 Lakh me best family car kaun si rahegi?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.name} - {self.phone}"