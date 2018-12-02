from django.contrib import admin
from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    search_fields = ('user', 'creating_date')
    list_display = ('user', 'creating_date', 'fav_product', 'fav_substitute')
    list_filter = ('user',)
