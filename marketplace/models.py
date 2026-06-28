from django.db import models

class AutoPart(models.Model):
    CONDITION_CHOICES = (
        ('NEW', 'New Part'),
        ('USED', 'Used Part'),
    )
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    compatible_cars = models.CharField(max_length=200, help_text="e.g., Swift, i20, Scorpio")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='NEW')
    # Is line ko dhundho aur 'upload_with' ki jagah 'upload_to' kar do
    image = models.ImageField(upload_to="parts/", blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.condition} ({self.price})"