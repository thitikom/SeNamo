from django import forms
from app.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404

#class add_product_form(forms.Form):
#    name = forms.CharField(max_length=50)
#    price = forms.IntegerField(min_value=0)
#    point = forms.IntegerField(min_value=0)
#    category = forms.ModelChoiceField(Category.objects.all())
#    description = forms.CharField(widget=forms.Textarea, required=False)
#    image = forms.FileField(required=False)

class add_profile_form(forms.Form):
    username = forms.CharField(required=False, max_length=50)
    first_name = forms.CharField(required=False, max_length=50)
    last_name = forms.CharField(required=False, max_length=50)
    birth_date = forms.DateField(required=False)
    CHOICES = (('0', 0), ('1', 1), ('2', 2),)
    sex = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=CHOICES)
    tel = forms.CharField(required=False, max_length=30)
    email = forms.EmailField(required=False, max_length=50)
    creditcard = forms.CharField(required=False, min_length=16, max_length=16)
    is_change_password = forms.BooleanField(required=False)
    old_password = forms.CharField(required=False, max_length=50)
    new_password = forms.CharField(required=False, max_length=50)
    confirm_password = forms.CharField(required=False, max_length=50)

    def clean_creditcard(self):
        if 'creditcard' in self.cleaned_data:
            return self.cleaned_data['creditcard']
        raise forms.ValidationError("Ensure Credit Card Number has at least 16 characters (it has 1).")
    def clean_confirm_password(self):
        if not 'is_change_password' in self.data or not self.data['is_change_password']:
            return ''
        if 'new_password' in self.data:
            new_password = self.data['new_password']
            confirm_password = self.data['confirm_password']
            if new_password == confirm_password:
                return confirm_password
        raise forms.ValidationError("Password do not match.")

    def clean_old_password(self):
        if not 'is_change_password' in self.data or not self.data['is_change_password']:
            return ''
        try:
            usernameData = self.data['username']
            user = get_object_or_404(User,username=usernameData)
            if(user.check_password(self.data['old_password'])):
                return self.data['old_password']
            else:
                raise forms.ValidationError("Incorrect Password.")
        except ObjectDoesNotExist:
            raise forms.ValidationError("Username '%s' does not exist." % usernameData)

class add_product_form(forms.ModelForm):
    class Meta:
        model = Product

class add_category_form(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, required=False)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,label="Username")
    password = forms.CharField(widget=forms.PasswordInput,label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput,label='Confirm password')
    email = forms.EmailField(label='Email')
    confirm_email = forms.EmailField(label='Confirm email')

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
    country = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=20)

class credit_card_form(forms.Form):
    card_number = forms.CharField(max_length=19, required=False)
    ccv = forms.CharField(max_length=4,label='ccv')

class loginEmp_form(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class add_supplier_form(forms.ModelForm):
    class Meta:
        model = Supplier

class search_form(forms.Form):
    q = forms.CharField(max_length=50)
    category = forms.ModelChoiceField(queryset=Category.objects.all())

class stockNormal_manage_form(forms.ModelForm):
    amount = forms.IntegerField()

orderSup_status_list = [("None",'None'),("Not ordered yet",'Not ordered yet'),("Has been ordered",'Has been ordered')]
class stockEmpty_manage_form(forms.ModelForm):
    amount = forms.IntegerField()
    status = forms.ChoiceField(choices=orderSup_status_list)
