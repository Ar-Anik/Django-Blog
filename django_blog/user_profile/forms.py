from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password", )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model

        user = model.objects.filter(username__iexact=username)

        if user.exists():
            raise forms.ValidationError("A User With That Name Already Exists")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model

        user = model.objects.filter(email__iexact=email)

        if user.exists():
            raise forms.ValidationError("A User With That Email Already Exists")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords Don't Match")

        return password

