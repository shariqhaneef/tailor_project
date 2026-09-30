from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Body measurements
    chest = models.IntegerField(null=True, blank=True)
    waist = models.IntegerField(null=True, blank=True)
    shoulder_width = models.IntegerField(null=True, blank=True)
    
    # Standard text fields for local addresses
    state = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"