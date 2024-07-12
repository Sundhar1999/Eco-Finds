from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserRegistration

@receiver(post_save, sender=User)
def create_user_registration(sender, instance, created, **kwargs):
    if created:
        UserRegistration.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_registration(sender, instance, **kwargs):
    try:
        instance.userregistration.save()
    except UserRegistration.DoesNotExist:
        # Handle the case where UserRegistration does not exist
        UserRegistration.objects.create(user=instance)
