#! /usr/bin/env python3
# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .db_request import select_favorites, select_substitutes, save_favorite_in_db, delete_favorite_in_db


@login_required
def favorites_list(request):
    user_favorites = select_favorites(request.user)
    context = {
        "favorites": user_favorites,
    }
    return render(request, 'favorite/favorites.html', context)


@login_required
def display_favorite(request, product_id):
    product, substitutes = select_substitutes(request.user, product_id)
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
        "substitutes" : substitutes_pag,
        "paginate": True,
        "checked": True
    }
    return render(request, 'product/substitutes_list.html', context)


@login_required
def save_favorite(request, product_id, substitute_id):
    save_favorite_in_db(request.user, product_id, substitute_id)
    return HttpResponse("save")


@login_required
def delete_favorite(request, product_id, substitute_id):
    delete_favorite_in_db(request.user, product_id, substitute_id)
    return HttpResponse("delete")

