#! /usr/bin/env python3
# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Favorite(models.Model):

    class Meta:
        """ unique index """
        unique_together = (('user', 'fav_product', 'fav_substitute'),)

    user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
    fav_product = models.ForeignKey(
           Product, related_name='fav_product_product',
        default='', on_delete=models.CASCADE)
    fav_substitute = models.ForeignKey(
           Product, related_name='fav_substitute_product',
        default='', on_delete=models.CASCADE)
    creating_date = models.DateTimeField(auto_now_add=True)
