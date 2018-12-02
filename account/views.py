#! /usr/bin/env python3
# coding: utf-8

from django.shortcuts import render
from registration.backends.default.views import RegistrationView
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import SignupForm

# Registration View
class AppRegistrationView(RegistrationView):
    form_class = SignupForm

    def register(self, form_class):
        new_user = super(AppRegistrationView, self).register(form_class)
        user_profile = UserProfile()
        user_profile.user = new_user
        user_profile.gender = form_class.cleaned_data['gender']
        user_profile.save()
        return user_profile

# VIEWS
def wait_confirm(request):
    return render(request, 'registration/activation_email_send.html')

@login_required
def my_account(request):
    return render(request, 'account/my_account.html')
