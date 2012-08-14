from django.db import models

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
    category = models.ForeignKey(Category,blank=True)
    description = models.TextField(max_length=300)
    image = models.FileField(upload_to='product_img/')

    def __unicode__(self):
        return self.name

    def thumbnail(self):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="50" /></a>""" % (
            (self.image.name, self.image.name))
    thumbnail.allow_tags = True
