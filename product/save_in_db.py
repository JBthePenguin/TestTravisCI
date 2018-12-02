#! /usr/bin/env python3
# coding: utf-8

from .models import Product


def save_product(product_api):
    """ save a product from API in DB """
    # check if the product is in DB
    try:
        product = Product.objects.get(code=product_api["code"])
    except Product.DoesNotExist:
        # save product in DB after except all Errors
        try:
            brands = product_api["brands"]
        except KeyError:
            brands = ""
        try:
            image_url = product_api["image_url"]
        except KeyError:
            image_url = ""
        try:
            image_small_url = product_api["image_url"]
        except KeyError:
            image_small_url = ""
        try:
            nutrient_level = product_api["nutrient_levels"]
        except KeyError:
            fat = None
            salt = None
            sugars = None
            saturated_fat = None
        else:
            try:
                fat = nutrient_level["fat"]
            except (ValueError, KeyError):
                fat = None
            try:
                salt = nutrient_level["salt"]
            except (ValueError, KeyError):
                salt = None
            try:
                saturated_fat = nutrient_level["saturated-fat"]
            except (ValueError, KeyError):
                saturated_fat = None
            try:
                sugars = nutrient_level["sugars"]
            except (ValueError, KeyError):
                sugars = None
        try:
            nutriments = product_api["nutriments"]
        except KeyError:
            fat_100g = None
            salt_100g = None
            saturated_fat_100g = None
            sugars_100g = None
        else:
            try:
                fat_100g = float(nutriments["fat_100g"])
            except (ValueError, KeyError):
                fat_100g = None
            try:
                salt_100g = float(nutriments["salt_100g"])
            except (ValueError, KeyError):
                salt_100g = None
            try:
                saturated_fat_100g = float(nutriments["saturated-fat_100g"])
            except (ValueError, KeyError):
                saturated_fat_100g = None
            try:
                sugars_100g = float(nutriments["sugars_100g"])
            except (ValueError, KeyError):
                sugars_100g = None
        product = Product(
            code=product_api["code"],
            product_name=product_api["product_name"],
            categories=product_api["categories"],
            brands=brands,
            nutrition_grades=product_api["nutrition_grades"],
            url=product_api["url"],
            image_url=image_url,
            image_small_url=image_small_url,
            fat=fat,
            salt=salt,
            saturated_fat=saturated_fat,
            sugars=sugars,
            fat_100g=fat_100g,
            saturated_fat_100g=saturated_fat_100g,
            sugars_100g=sugars_100g,
            salt_100g=salt_100g,)
        product.save()
