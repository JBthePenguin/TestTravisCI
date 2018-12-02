#! /usr/bin/env python3
# coding: utf-8

import openfoodfacts
from requests.exceptions import ConnectionError
from .models import Product
from product.save_in_db import save_product


def found_product(search_term):
    """ make request to API openfoodfacts to found a product """
    # API request
    try:
        search_result = openfoodfacts.products.search(
            search_term, locale="fr"
        )
    except ConnectionError:
        product = "API connect error"
    else:
        products = search_result['products']
        if len(products) == 0:
            # check if there is a result ...
            product = "api no result"
        else:
            i = 0
            prod_founded = False
            while not prod_founded:
                try:
                    product = products[i]
                except IndexError:
                    # check if there is a result ...
                    product = "api no result"
                    prod_founded = True
                else:
                    try:
                        product["nutrition_grades"]
                    except KeyError:
                        i += 1
                    else:
                        prod_founded = True
    return product


def found_substitutes(product_code):
    """ make request to API openfoodfacts to found substitutes """
    product = Product.objects.get(code=product_code)
    list_categories = product.categories.split(",")
    i = 1
    substitutes = []
    while i < 3:
        # search substitute in the 2 last categories 
        try:
            category = list_categories[-i]
        except IndexError:
            break
        if category[0] == " ":
            # remove space
            category = category[1:]
        # request API openfoodfacts to found products in same category
        new_substitutes = openfoodfacts.products.get_by_category(
            category, locale="fr")
        # remove the similar products
        subs = []
        for new_substitute in new_substitutes:
            add_sub = True
            if product.product_name in new_substitute["product_name"]:
                add_sub = False
            else:
                # remove product without or bad nutriscore
                try:
                    new_substitute["nutrition_grades"]
                except KeyError:
                    add_sub = False
                else:
                    if new_substitute["nutrition_grades"] > product.nutrition_grades:
                        add_sub = False
                    else:
                        for substitute in substitutes:
                            if substitute.code == new_substitute["code"]:
                                add_sub = False
            if add_sub:
                subs.append(new_substitute)
        for sub in subs:
            save_product(sub)
            substitutes.append(Product.objects.get(code=sub["code"]))
        i += 1
    if len(substitutes) != 0:
        substitutes.sort(key=lambda x: x.nutrition_grades)
    return product, substitutes
