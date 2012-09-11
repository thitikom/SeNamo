from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=300)
    image = models.FileField(upload_to='product_img/')

    def __unicode__(self):
        return self.name

    def thumbnail(self):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="50" /></a>""" % (
            (self.image.name, self.image.name))
    thumbnail.allow_tags = True

# We use the same table to keep Customer and Employee
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    creditcard = models.CharField(max_length=50)
    point = models.IntegerField(default=0)

    # for those who are employee
    manager = models.BooleanField(default = False)
    clerk = models.BooleanField(default = False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Order(models.Model):
    user = models.ForeignKey(User)
    status = models.CharField(max_length=50)
    timestamp = models.TimeField(auto_now_add=True)

class ProductInOrder(models.Model):
    product = models.ForeignKey(Product)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=50)
    ship_time = models.TimeField()
    order = models.ForeignKey(Order)