from django.dispatch import receiver
from django.db.models.signals import post_save
from authapp.models import Profile,User

# NOTE:  i did the signal so when we have a user created we automaticlly create a profile 
@receiver(post_save,sender=User)
def create_profile_for_user(sender,instance,created,**kwargs):
    if created:
        return Profile.objects.create(user=instance,username=instance.username,
                                      first_name=instance.first_name,
                                      last_name=instance.last_name,
                                      email=instance.email)
