#! /usr/bin/env python3
# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # Extend User model with a new field -> gender
    gender = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
