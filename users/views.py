# from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
import random
import string
from django.shortcuts import redirect
from django.urls import reverse
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


import random
import string
import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from users.forms import RegisterForm, ProfileForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView

from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse

from config.settings import EMAIL_HOST_USER


"""class UserViewSet(ModelViewSet):
    # ModelViewSet provides default
    # create, retrieve, update, partial_update, destroy and list

    queryset = User.objects.all()
    serializer_class = UserSerializer"""


class RegisterView(CreateView):

    model = User
    form_class = RegisterForm

    """ # token approve via email
    
    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}'

        send_mail(
            "Skystore - email confirm",
            f"To confirm the email please tap on the link: {url}",
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return super().form_valid(form)"""

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        return super().form_valid(form)


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        return self.request.user


"""def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    return redirect(reverse("users:login"))
"""


class UserProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:user-detail')

    def get_object(self, queryset=None):
        return self.request.user


class UserResetPasswordView(PasswordResetView):
    model = User
    form_class = PasswordResetForm
    template_name = 'users/password_reset.html'

    def form_valid(self, form):

        form_email = form.cleaned_data.get("email")
        user = User.objects.get(email=form_email)

        ### new pass

        characters = string.ascii_letters + string.digits + string.punctuation
        new_password = ''.join(random.choice(characters) for _ in range(10))
        # password = User.objects.make_random_password(10)  # ?????

        user.set_password(new_password)
        user.save()

        ### send email

        send_mail(
            "Heroes CRM - new password generated",
            f"Please use the below password: {new_password}",
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return redirect(reverse("users:login"))


class UserResetPasswordDoneView(PasswordResetView):
    model = User
    form_class = PasswordResetForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:login')


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_all_users'


@permission_required('users.deactivate_user')
def user_change_active(request, pk):
    user = User.objects.get(pk=pk)

    user.is_active = False if user.is_active else True
    user.save()

    return redirect(reverse('users:user-list'))

