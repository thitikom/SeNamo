from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.datetime_safe import date

# Create your models here.
class Supplier(models.Model):
    company_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=100)

    def __unicode__(self):
        return self.company_name

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
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
    image = models.FileField(upload_to='product_img/')
    amount = models.IntegerField(default=0)
    orderSupStatus = models.BooleanField(default=False)

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
    point = models.IntegerField(default=1000)
    sex = models.IntegerField(default=0) # 0 is undefine, 1 is male, 2 is female
    birthday = models.DateField(null=True)
    tel = models.CharField(max_length=30) #format 0xx-xxxxxxx... [should validate]


    #address
    addr_firstline = models.CharField(max_length=100)
    addr_secondline = models.CharField(max_length=100)
    addr_town = models.CharField(max_length=50)
    addr_country = models.CharField(max_length=50)
    addr_zipcode = models.CharField(max_length=15)

    # for those who are employee
    manager = models.BooleanField(default = False)
    clerk = models.BooleanField(default = False)

    def get_address(self):
        return {'firstline':self.addr_firstline,
                'secondline':self.addr_secondline,
                'town':self.addr_town,
                'country':self.addr_country,
                'zipcode':self.addr_zipcode,}

    def get_age(self):
        today = date.today()
        born = self.birthday
        try: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(year=today.year, day=born.day-1)
        except AttributeError:
            return 0
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Order(models.Model):
    user = models.ForeignKey(User)
    status = models.CharField(max_length=50)

    total_price = models.IntegerField()
    total_point = models.IntegerField()

    #address
    addr_firstline = models.CharField(max_length=100)
    addr_secondline = models.CharField(max_length=100)
    addr_town = models.CharField(max_length=50)
    addr_country = models.CharField(max_length=50)
    addr_zipcode = models.CharField(max_length=15)

    timestamp = models.DateTimeField(auto_now_add=True)

    def get_address(self):
        return {'firstline':self.addr_firstline,
                'secondline':self.addr_secondline,
                'town':self.addr_town,
                'country':self.addr_country,
                'zipcode':self.addr_zipcode,}

    def __unicode__(self):
        return unicode(self.id) + ': ' + unicode(self.user.username)

class ProductInOrder(models.Model):
    product = models.ForeignKey(Product)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=50)
    ship_time = models.DateTimeField(blank=True,null=True)
    order = models.ForeignKey(Order)
