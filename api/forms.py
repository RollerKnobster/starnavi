from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Incorrect username or password')
        if not user.check_password(password):
            raise forms.ValidationError('Incorrect username or password')

    def save(self):
        auth = authenticate(**self.cleaned_data)
        return auth


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)

    def clean_username(self):
        try:
            if User.objects.get(username=self.cleaned_data['username']):
                raise forms.ValidationError(
                    'User already exists with this username.'
                )
        except User.DoesNotExist:
            pass
        return self.cleaned_data['username']

    def clean_password(self):
        password = self.cleaned_data['password']
        self.raw_password = password
        return make_password(password)

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user
