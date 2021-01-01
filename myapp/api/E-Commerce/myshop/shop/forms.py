
from django.contrib.auth.models import User
from django import forms
from shop.models import Customer,Product,ShippingAddress,CartItem
from django.contrib.auth.forms import UserCreationForm

class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields=('address','city','state','zipcode')

class UserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)

    class Meta:
        model = User
        fields = ('username','first_name','last_name')
