#! /usr/bin/env python3
# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationFormUniqueEmail


# SIGNUP FORM
class SignupForm(RegistrationFormUniqueEmail):
    """ extend the UserCreationForm """
    gender = forms.CharField(
        widget=forms.RadioSelect(
            choices=[(True, 'Girl'), (False, 'Boy')]
        ),
        error_messages={
            'required':"C'est l'un ou l'autre, mais pas aucun ... ni les deux."
        },
        label='',
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # custom fields
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['password1'].label = "Mot de passe (min 8 caractères):"

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'gender',
        )
