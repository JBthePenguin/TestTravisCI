#! /usr/bin/env python3
# coding: utf-8

from django.urls import path, re_path, include
from registration.backends.default.views import RegistrationView
from . import views


urlpatterns = [
    re_path(
        r'^register/$',
        views.AppRegistrationView.as_view(success_url='../wait_confirm/'),
        name='registration_register'
    ),
    path('', include('registration.backends.default.urls')),
    path('my_account/', views.my_account),
    path('wait_confirm/', views.wait_confirm),
]
