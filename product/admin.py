from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Product
from favorite.models import Favorite


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('id', 'product_name', 'brands', 'code')
    list_display = ('id', 'product_name', 'brands', 'code')
    change_list_template = "product/product_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('update_db/', self.update_db), ]
        return my_urls + urls

    def update_db(self, request):
        """ delete product not using in favorite """
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
        self.message_user(request, "Base de données mise à jour")
        return HttpResponseRedirect("../")
