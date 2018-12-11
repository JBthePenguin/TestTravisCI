from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from product.models import Product
from django.core.management import call_command


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
        call_command('update_db')
        self.message_user(request, "Base de données mise à jour")
        return HttpResponseRedirect("../")
