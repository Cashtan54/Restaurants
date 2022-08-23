from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):

    def __str__(self):
        return self.username


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    menu_as_link = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restaurants', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, owner: {self.owner}'


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='votes', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user} > {self.restaurant} {self.date}'

    class Meta:
        unique_together = ('user', 'date')
