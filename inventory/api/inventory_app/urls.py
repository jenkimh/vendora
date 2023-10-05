from django.urls import path

from inventory_app.views import api_list_products, api_product_detail, api_list_categories

urlpatterns = [
    path("products/", api_list_products, name="api_list_products"),
    path(
        "products/<int:id>/",
        api_product_detail,
        name="api_product_detail",
    ),
     path(
        "category/",
        api_list_categories,
        name="api_list_categories",
    ),

]
