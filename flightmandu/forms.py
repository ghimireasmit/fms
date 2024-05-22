from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserSignupForm(forms.Form):
    userFname = forms.CharField(label='First Name', max_length=100)
    userLname = forms.CharField(label='Last Name', max_length=100)
    userEmail = forms.EmailField(label='Email')
    userPhone = forms.CharField(label='Phone', max_length=20)
    userPassword = forms.CharField(label='Password', widget=forms.PasswordInput)
    userCpassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('userPassword')
        confirm_password = cleaned_data.get('userCpassword')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    

class airlineSignupForm(forms.Form):
    airlineName = forms.CharField(label='Name', max_length=100)
    airlineEmail = forms.EmailField(label='Email')
    airlinePhone = forms.CharField(label='Phone', max_length=20)
    airlinePassword = forms.CharField(label='Password', widget=forms.PasswordInput)
    airlineCpassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    airlineImage = forms.ImageField(label='Profile Image', required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('airlinePassword')
        confirm_password = cleaned_data.get('airlineCpassword')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class PassengerDetailsForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    passport_number = forms.CharField(max_length=50, required=False)
    nationality = forms.CharField(max_length=50, required=False)

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']


from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'full-width form-input', 'placeholder': 'Old Password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'full-width form-input', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'full-width form-input', 'placeholder': 'Confirm Password'})
        
        # Optionally customize help_text for better user experience or remove it.
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None

