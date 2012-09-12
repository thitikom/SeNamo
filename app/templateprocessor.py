__author__ = 'khemin'

from app.models import Category

def category(request):
    return {'category_list' : Category.objects.all()}