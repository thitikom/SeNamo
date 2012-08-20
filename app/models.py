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

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    creditcard = models.CharField(max_length=50)
    point = models.IntegerField(default=0)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)