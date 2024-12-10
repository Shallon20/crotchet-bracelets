from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Full Name'}), required=True)
    shipping_email = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Email'}), required=True)
    shipping_address1 = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Address 1'}), required=True)
    shipping_address2 = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Address 2'}), required=False)
    shipping_city = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping City'}), required=True)
    shipping_state = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping State'}), required=False)
    shipping_zipcode = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Zipcode'}), required=False)
    shipping_country = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state','shipping_zipcode', 'shipping_country']

        exclude = ['user']