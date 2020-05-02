from django.db import models
from django.contrib.auth.models import User
# from cloudinary_storage.storage import VideoMediaCloudinaryStorage
# from cloudinary_storage.validators import validate_video

class Film(models.Model):
    RATING_STARS = (
    ("⭐️", "⭐️"),
    ("⭐️⭐️", "⭐️⭐️"),
    ("⭐️⭐️⭐️", "⭐️⭐️⭐️"),
    ("⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️"),
    ("⭐️⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️⭐️"),
)
    title = models.CharField(max_length=255, null=False)
    rating = models.CharField(
        max_length=20,
        choices=RATING_STARS,
        default="",
    )
    description = models.TextField(max_length=255)
    thumbnail = models.ImageField(upload_to='images/', blank=True) 
    videofile = models.ImageField(upload_to='videos/', blank=True)

    def __str__(self):
        return self.title

class user_history(models.Model):
    user = models.ForeignKey(User, default=1, verbose_name="Category", on_delete=models.CASCADE)
    history = models.TextField(max_length = 1000, null=True, blank = True)

    def __str__(self):
        return self.user.username
        
    def append_history(self, new_order):
        history_list = self.history.split()
        history_list.append(new_order)
        history_list = list(dict.fromkeys(history_list))
        self.history = " ".join(history_list)
        self.save()

    def get_history(self):
        history_list = self.history.split()
        return history_list