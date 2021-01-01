from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    city = models.CharField(blank=True,max_length=100)
    country = models.CharField(blank=True,max_length=100)
    age = models.CharField(blank=True,max_length=100)
    profile_image = models.ImageField(blank=True,null=True,upload_to='images/')

    def get_absolute_url(self):
        return reverse('myapp:detail',kwargs={'pk':self.pk})

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True,upload_to='posts/')
    name = models.CharField(max_length=100)
