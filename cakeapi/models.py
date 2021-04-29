from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse

from datetime import datetime
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
# # Create your models here.

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print(reset_password_token.user.email)
    email_plaintext_message = " copy this token------->token={}".format(reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        'jastestpass@gmail.com',
        # to:
        [reset_password_token.user.email])


class Cake(models.Model):
    cakeid = models.AutoField(primary_key=True , unique=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='cake/images' , default="")
    price = models.IntegerField()
    weight = models.IntegerField()
    eggless = models.BooleanField()
    ingredients = models.CharField(max_length =200)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=70)
    rating = models.IntegerField()

    def __str__(self):
        return self.name

class Carts(models.Model):
    # userid = models.OneToOneField(User , on_delete=models.CASCADE)
    cakeid = models.IntegerField(default="")

    name =   models.CharField(max_length=200)
    price =  models.IntegerField()
    image =  models.ImageField(upload_to="cake/images" , default="")
    weight = models.IntegerField()
    email =  models.EmailField()

    def __str__(self):
        return  self.name

# class Order(models.Model):
#     user_id = models.ForeignKey(User,on_delete=models.CASCADE)
#     name = models.ManyToManyField(Cake)

class Checkout(models.Model):
    orderid = models.AutoField(primary_key =True)
    name = models.CharField(max_length=200)
    phone = models.IntegerField()
    city = models.CharField(max_length=200)
    pincode =models.IntegerField()
    state = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    price = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name
    
    # cakes = models.ManyToManyField(Cake ,blank=True)


class CheckoutFinal(models.Model):
    orderid = models.AutoField(primary_key=True)
    orderdate = models.DateTimeField(default=datetime.now, blank=True)
    name = models.CharField(max_length=200)
    phone = models.IntegerField()
    city = models.CharField(max_length=200)
    pincode = models.IntegerField()
    state = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    price = models.IntegerField()
    email = models.EmailField()
    cakes = models.ManyToManyField(Carts, blank=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    image=models.ImageField(upload_to="cakeapi/images")

class AddOrder(models.Model):
    
    name = models.CharField(max_length=200)
    phone = models.IntegerField()
    city = models.CharField(max_length=200)
    pincode =models.IntegerField()
    state = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    price = models.IntegerField()
    email = models.EmailField()
    cakes = models.ManyToManyField(Carts ,blank=True)

    def __str__(self):
        return self.name