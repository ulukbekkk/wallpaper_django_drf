from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.title

    def save(self):
        self.slug = self.title.lower().replace(' ', '')
        return super().save()


class Wallpaper(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='wallpaper')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='wallpaper')

    image = models.ImageField('Обои', upload_to='wallpaper', null=False)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.CASCADE, related_name='comment')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.CASCADE, related_name='like')


class Rating(models.Model):
    choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.CASCADE, related_name='rating')
    value = models.IntegerField(choices=choices)
