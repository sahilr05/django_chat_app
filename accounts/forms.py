from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import Interest

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}),
        required=True,
    )

    confirm_password = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}),
        required=True,
    )

    class Meta:
        model = User
        fields = ("phone_number", "name", "email", "gender", "country", "password", "confirm_password")


class EmailPhoneLoginForm(forms.Form):
    email_or_phone = forms.CharField(label='Email or phone number', max_length=100)
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))


    # def clean(self):
    #     cleaned_data = super().clean()
    #     email_or_phone = cleaned_data.get('email_or_phone')
    #     password = cleaned_data.get('password')

    #     # Perform any additional validation here if needed

    #     return cleaned_data


class MyAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "username")


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}),
        required=True,
    )


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "type": "text"})
        }
        fields = ("name",)
