#! /usr/bin/env python3
# coding: utf-8

from product.models import Product
from .models import Favorite

def select_favorites(user):
    """ select all favorites for a specific account
    and return a list of them """
    # select all account's favorites in db
    all_favorites = Favorite.objects.all()
    # construct favorite :
    # [[prod, sub1], [prod, sub2]] -> [prod, sub1, sub2] -> [prod, [sub1, sub2]]
    # construct favorites : [favorite]
    # account_favorites -> favorites -> user_favorites
    # account_favorites : [[prod, sub1], [prod, sub2]]
    account_favorites = []
    for favorite in all_favorites:
        if favorite.user.id == user.id:
            account_favorites.append(favorite)
    # favorites : [prod, sub1, sub2]
    favorites = []
    for account_favorite in account_favorites:
        favorite_added = False
        substitute = Product.objects.get(id=account_favorite.fav_substitute.id)
        for favorite in favorites:
            if account_favorite.fav_product.id == favorite[0].id:
                # this product have a favorite
                favorite.append(substitute)
                favorite_added = True
                break
        if favorite_added is False:
            # create a new favorite for this product
            product = Product.objects.get(id=account_favorite.fav_product.id)
            favorite = [product, substitute]
            favorites.append(favorite)
    # user_favorites : [prod, [sub1, sub2]]
    user_favorites = []
    for favorite in favorites:
        user_favorite = []
        # place product indice 0
        user_favorite.append(favorite[0])
        # make a list of substitutes
        substitutes = []
        for substitute in favorite[1:]:
            substitutes.append(substitute)
        user_favorite.append(substitutes)
        user_favorites.append(user_favorite)
    return user_favorites


def select_substitutes(user, product_id):
    """ Construct a favorite (product, substitutes) with
    the product id """
    # select substitutes saved for this product in db
    product = Product.objects.get(id=product_id)
    all_favorites = Favorite.objects.all()
    account_favorites = []
    for favorite in all_favorites:
        if (
            favorite.user.id == user.id) and (
            favorite.fav_product.id == product_id
        ):
            account_favorites.append(favorite)
    substitutes = []
    for favorite in account_favorites:
        substitute = Product.objects.get(id=favorite.fav_substitute.id)
        substitutes.append(substitute)
    return product, substitutes


def save_favorite_in_db(user, product_id, substitute_id):
    Favorite.objects.create(
        user = user,
        fav_product = Product.objects.get(id=product_id),
        fav_substitute = Product.objects.get(id=substitute_id),
    )


def delete_favorite_in_db(user, product_id, substitute_id):
    Favorite.objects.filter(
        user = user,
        fav_product = Product.objects.get(id=product_id),
        fav_substitute = Product.objects.get(id=substitute_id),
    ).delete()