from django.contrib.auth.models import User
from userhome.models import user_history
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_history(sender, instance, **kwargs):
    if User.is_authenticated and user_history.objects.filter(user=instance).exists() == False:
        userHIS = user_history(user=instance, history="")
        userHIS.save()
post_save.connect(create_user_history, sender=User)