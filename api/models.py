from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
class UserProfile(models.Model):
    STANDARD = 'STD'
    PREMIUM = 'VIP'
    PROFILE_LEVEL_CHOICES = (
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
    )
    
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    display_name = models.CharField(max_length=50)
    profile_level = models.CharField(max_length=3, choices=PROFILE_LEVEL_CHOICES, default=STANDARD)
    
    
class Checklist(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='checklists')
    
    def __str__(self) -> str:
        return self.title
    
class Item(models.Model):
    text = models.CharField(max_length=30)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    done = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return ('V' if self.done else 'X') + ' ' + self.text