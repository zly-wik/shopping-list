from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import UserProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])