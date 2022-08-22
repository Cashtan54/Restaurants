from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


def save_restaurant_menu(instanse, filename):
    return f'{instanse.name}.{filename.split(".")[-1]}'


class User(AbstractUser):

    def __str__(self):
        return self.username


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    menu_as_link = models.CharField(max_length=255, blank=True, null=True)
    menu_as_file = models.FileField(blank=True, null=True, upload_to=save_restaurant_menu)
    last_update = models.DateField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restaurants', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, owner: {self.owner}'


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='votes', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'restaurant', 'date')
