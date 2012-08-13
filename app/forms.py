from django import forms
from app.models import Category, Product

#class add_product_form(forms.Form):
#    name = forms.CharField(max_length=50)
#    price = forms.IntegerField(min_value=0)
#    point = forms.IntegerField(min_value=0)
#    category = forms.ModelChoiceField(Category.objects.all())
#    description = forms.CharField(widget=forms.Textarea, required=False)
#    image = forms.FileField(required=False)

class add_product_form(forms.ModelForm):
    class Meta:
        model = Product

class add_category_form(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, required=False)