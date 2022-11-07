from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MyRoom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='my_room')
    first_name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    about_self = models.TextField(blank=True)
    image = models.ImageField(verbose_name='images', upload_to='user_img', default='media/default.png')

    def __str__(self):
        return self.first_name