from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from chi.models import LichessAccount


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', min_length=4, max_length=150)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    lichess_account = forms.CharField(label='Lichess Account', min_length=1, max_length=20)
    email = forms.EmailField(label='Email')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        existing_usernames = User.objects.filter(username=username)
        if existing_usernames.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        existing_emails = User.objects.filter(email=email)
        if existing_emails.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2
    
    # TODO: Add validation for lichess account being real.
    # def clean_lichess_account(self):
    #     lichess_account = self.cleaned_data['lichess_account'].lower()
    #     existing_accounts = LichessAccount.objects.filter(username=lichess_account)
    #     if not existing_accounts.count():
    #         new_account = LichessAccount()
    #     return lichess_account

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )

        lichess_username = self.cleaned_data['lichess_account'].lower()
        lichess_account = LichessAccount(user=user, username=lichess_username)
        lichess_account.save()

        return user