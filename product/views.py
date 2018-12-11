#! /usr/bin/env python3
# coding: utf-8

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from product.search_request import found_product, found_substitutes
from favorite.db_request import select_substitutes
from product.save_in_db import save_product
from .models import Product


# VIEWS
def index(request, alert_message=False):
    """ return the home page """
    context = {
        "alert_message": alert_message,
    }
    return render(request, 'product/index.html', context)


def search_product(request):
    """ request API Openfoodfacts, redirect to
    - index if no result
    - substitutes_list (search_substitutes()) with result """
    search_term = request.GET.get('search_term')
    product = found_product(search_term)
    if product in ["API connect error", "api no result", "db no result"]:
        return index(request, product)
    # save product in db
    save_product(product)
    return redirect('substitutes_list', product["code"])


def search_substitutes(request, product_code):
    """ request API Openfoodfacts to found substitutes and
    return the page with pagination (6 elts) """
    product, substitutes = found_substitutes(product_code)
    sub_ids_saved_in_fav = []
    if request.user.is_authenticated:
        # found if user have favorite with this product and substitutes
        fav_product, fav_substitutes = select_substitutes(
            request.user, product.id)
        for fav_substitute in fav_substitutes:
            for substitute in substitutes:
                if fav_substitute == substitute:
                    sub_ids_saved_in_fav.append(fav_substitute.id)
    # if substitutes.count() == 0:
    if len(substitutes) == 0:
        substitutes_pag = False
    else:
        paginator = Paginator(substitutes, 6)
        page = request.GET.get('page')
        try:
            substitutes_pag = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            substitutes_pag = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            substitutes_pag = paginator.page(paginator.num_pages)
    context = {
        "product": product,
        "substitutes": substitutes_pag,
        "paginate": True,
        "substitutes_saved": sub_ids_saved_in_fav,
        "checked": False
    }
    return render(request, 'product/substitutes_list.html', context)


def description(request, product_id):
    """ return the page with description of one product """
    product = Product.objects.get(id=product_id)
    # remove .0 if no decimal product
    if str(product.fat_100g)[-2:] == ".0":
        product.fat_100g = int(product.fat_100g)
    if str(product.salt_100g)[-2:] == ".0":
        product.salt_100g = int(product.salt_100g)
    if str(product.saturated_fat_100g)[-2:] == ".0":
        product.saturated_fat_100g = int(product.saturated_fat_100g)
    if str(product.sugars_100g)[-2:] == ".0":
        product.sugars_100g = int(product.sugars_100g)
    context = {
        "product": product
    }
    return render(request, 'product/product.html', context)


def error_404(request, exception):
    return render(request, 'error/404.html', status=404)


def mentions(request):
    return render(request, 'product/mentions.html')
