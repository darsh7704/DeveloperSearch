from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Create profile automatically when a user is created
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        print('Profile signal triggered')
        Profile.objects.create(
            user=instance,  
            username=instance.username,
            email=instance.email,
            name=instance.first_name
        )

# Delete user if the profile is deleted
@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()