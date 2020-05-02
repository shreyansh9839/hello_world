from django.contrib.auth.models import User
from userhome.models import user_history
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_history(sender, instance, **kwargs):
    if created and not user_history.objects.exists(user=instance):
        user_history = user_history(user=instance)
        userhistory.save()

post_save.connect(create_user_history, sender=User)