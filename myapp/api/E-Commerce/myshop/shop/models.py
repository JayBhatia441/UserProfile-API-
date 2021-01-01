from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ckeditor.fields import RichTextField
import uuid
# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.user.username



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(blank=True,null=True,upload_to="images/")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:detail',kwargs={'pk':self.pk})



class CartItem(models.Model):
    cart = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    total = models.FloatField(null=True,blank=True,default=0)
    ordered = models.BooleanField(default=False)
    transaction_id = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)









class Order(models.Model):
    order = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    total = models.FloatField(null=True,blank=True)
    ordered = models.BooleanField(default=False)
    transaction_id = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.transaction_id)

class ShippingAddress(models.Model):
    customer = models.OneToOneField(User,on_delete=models.CASCADE)

    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state= models.CharField(max_length=250)
    zipcode = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    def get_absolute_url(self):
        return reverse('shop:update',kwargs={'pk':self.pk})
