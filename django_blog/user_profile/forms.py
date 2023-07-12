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

class UserProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)

        if user.exists():
            raise forms.ValidationError("A User With That Name Already Exists")

        print('Clean Data User Profile Update Form : ', self.cleaned_data)

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)

        if user.exists():
            raise forms.ValidationError("A User With That Email Already Exists")

        return email

    def change_password(self):
        print("Self Data User Profile Update Form : ", self.data)
        if 'new_password' in self.data and 'confirm_password' in self.data:
            new_password = self.data.get('new_password')
            confirm_password = self.data.get('confirm_password')

            if new_password != '' and confirm_password != '':
                if new_password != confirm_password:
                    raise forms.ValidationError("Password Don't Match")
                else:
                    self.instance.set_password(new_password)
                    self.instance.save()

    def clean(self):
        self.change_password()

class ProfilePictureUpdateForm(forms.Form):
    profile_image = forms.ImageField(required=True)
