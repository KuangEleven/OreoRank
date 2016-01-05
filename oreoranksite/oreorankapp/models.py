from django.db import models
from django.contrib.auth.models import User

class Cookie(models.Model):
    def __str__(self):
       return self.name
    name = models.CharField(max_length=200)

class CookieScore(models.Model):
    def __str__(self):
       return self.user.username + ' ' + self.cookie.name
    cookie = models.ForeignKey(Cookie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()