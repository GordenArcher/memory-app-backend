from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='memories')
    description = models.TextField(max_length=100000, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class ProfilePic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profilePic')