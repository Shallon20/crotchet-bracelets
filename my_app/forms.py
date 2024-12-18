from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

from my_app.models import Product, Profile

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Phone'}), required=False)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address 1'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address 2'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'City'}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'State'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Zipcode'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Country'}), required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country')

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = 'Enter new password'
        self.fields['new_password1'].help_text = '<span class="glyphicon glyphicon-user"></span>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = 'Enter new password'
        self.fields['new_password2'].help_text = '<span class="glyphicon glyphicon-user"></span>'


class UpdateUserForm(UserChangeForm):
    # hide password stuff
    password = None
    # get other fields
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = 'username'
        self.fields['username'].help_text = '<span class="glyphicon glyphicon-user"></span>'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'image',
            'category',
            'is_new'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message', 'rows': 5})
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
