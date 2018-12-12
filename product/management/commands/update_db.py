""" delete product not using in favorite """
from django.core.management.base import BaseCommand
from product.models import Product
from favorite.models import Favorite


class Command(BaseCommand):
    help = 'Update the database'

    def handle(self, *args, **kwargs):
        # make a list of product id used
        all_favorites = Favorite.objects.all()
        product_in_fav_ids = []
        for favorite in all_favorites:
            product_in_fav_ids.append(favorite.fav_product.id)
            product_in_fav_ids.append(favorite.fav_substitute.id)
        product_in_fav_ids = list(set(product_in_fav_ids))
        # delete product not used
        products_not_used = Product.objects.exclude(id__in=product_in_fav_ids)
        for product in products_not_used:
            product.delete()
