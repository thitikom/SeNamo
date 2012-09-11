from django import forms
from app.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


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

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    confirm_email = forms.EmailField()

    def clean_confirm_password(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password == confirm_password:
                return confirm_password
        raise forms.ValidationError("Password do not match.")

    def clean_confirm_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            confirm_email = self.cleaned_data['confirm_email']
            if email == confirm_email:
                return confirm_email
        raise forms.ValidationError("email do not match.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError("Username '%s' has already been used." % username)
        except ObjectDoesNotExist:
            return username
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("Email '%s' has already been used."%email)
        except ObjectDoesNotExist:
            return email

country_list = [("Thailand",'Thailand'),("Hong Kong",'Hong Kong')]

class address_form(forms.Form):
    first_line = forms.CharField(max_length=100)
    second_line = forms.CharField(max_length=100,required=False)
    town = forms.CharField(max_length=100)
    country = forms.ChoiceField(choices=country_list)
    zip_code = forms.CharField(max_length=20)

class credit_card_form(forms.Form):
    card_number = forms.CharField(max_length=19, required=False)
    ccv = forms.CharField(max_length=4,label='ccv')