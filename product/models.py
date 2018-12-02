#! /usr/bin/env python3
# coding: utf-8

from django.db import models


class Product(models.Model):
    code = models.CharField(max_length=255, null=True)
    product_name = models.CharField(db_index=True, max_length=255, null=True)
    brands = models.CharField(db_index=True, max_length=255, null=True)
    categories = models.CharField(db_index=True, max_length=500, null=True)
    nutrition_grades = models.CharField(db_index=True, max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    image_url = models.CharField(max_length=255, null=True)
    image_small_url = models.CharField(max_length=255, null=True)
    fat = models.CharField(max_length=255, null=True)
    salt = models.CharField(max_length=255, null=True)
    saturated_fat = models.CharField(max_length=255, null=True)
    sugars = models.CharField(max_length=255, null=True)
    fat_100g = models.FloatField(null=True)
    saturated_fat_100g = models.FloatField(null=True)
    sugars_100g = models.FloatField(null=True)
    salt_100g = models.FloatField(null=True)
