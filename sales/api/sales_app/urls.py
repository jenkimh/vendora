from django.urls import path

from sales_app.views import api_list_sales, api_show_sales

urlpatterns = [
    path("orders/", api_list_sales, name="api_list_sales"),
    path(
        "orders/<int:id>/",
        api_show_sales,
        name="api_show_sales"
    )
]
