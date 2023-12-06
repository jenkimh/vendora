from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
import pika

from common.json import ModelEncoder
from .models import CategoryVO, ProductVO, Address, Customer, Status, Payment, Cart, Order, OrderProduct
from .encoders import CustomerEncoder, AddressEncoder, OrderEncoder, StatusEncoder


@require_http_methods(["GET", "POST"])
def api_list_sales(request):
    if request.method == "GET":
        orders = Order.objects.all()
        return JsonResponse(
            {"orders": orders},
            encoder=OrderEncoder
        )
    else:
        content = json.loads(request.body)
        try:
            product = ProductVO.objects.get(id=content["product"])
            content["product"] = product
        except ProductVO.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid product"},
                status=400,
            )
        order = Order.objects.create(**content)
        return JsonResponse(
            order,
            encoder=OrderEncoder,
            safe=False,
        )

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_sales(request, id):
    if request.method == "GET":
        orders = Order.objects.get(id=id)
        return JsonResponse(
            orders,
            encoder=OrderEncoder,
            safe=False,
        )
    elif request.method == "PUT":
        content = json.loads(request.body)
        try:
            if "product" in content:
                product = ProductVO.objects.get(id=content["product"])
                content["product"] = product
        except ProductVO.DoesNotExist:
                return JsonResponse(
                {"message": "Invalid product"},
                status=400,
            )
        Order.objects.filter(id=id).update(**content)
        order = Order.objects.get(id=id)
        return JsonResponse(
            order,
            encoder=OrderEncoder,
            safe=False,
        )
    else:
        count, _ = Order.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
