from django.urls import path

from inventory_app.views import api_list_products, api_show_product, api_list_categories, api_show_category

urlpatterns = [
    path("products/", api_list_products, name="api_list_products"),
    path(
        "products/<int:id>/",
        api_show_product,
        name="api_show_product",
    ),
     path(
        "category/",
        api_list_categories,
        name="api_list_categories",
    ),
    path(
        "category/<int:id>/",
        api_show_category,
        name="api_show_category",
    ),

]
