from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('tg_id', 'email', 'password1', 'password2',)


class ProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('tg_id', 'email', 'first_name', 'last_name', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
