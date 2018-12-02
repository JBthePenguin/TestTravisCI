from django.urls import path

from . import views # import views so we can use them in urls.

urlpatterns = [
    path('', views.favorites_list),
    path('<int:product_id>/', views.display_favorite),
    path(
        'save/<int:product_id>/<int:substitute_id>/',
        views.save_favorite
    ),
    path(
        'delete/<int:product_id>/<int:substitute_id>/',
        views.delete_favorite
    ),
]
