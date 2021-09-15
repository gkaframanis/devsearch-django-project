from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

from .models import Profile
from django.contrib.auth.models import User


# The sender will be the model that actually sends this signal and instance the model object.
# created is boolean value, if the instance already existed or not.
# Any time a user is created, a profile will also get created.

# @receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user, username=user.username, email=user.email, name=user.first_name)


# @receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    # The instance here is the profile and from that we get the user.
    user = instance.user
    user.delete()


# A listener (receiver) for when a user is created.
post_save.connect(create_profile, sender=User)
# A listener for when a profile is deleted, so the user will get deleted too.
post_delete.connect(delete_user, sender=Profile)
