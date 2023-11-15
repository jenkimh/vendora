from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
import pika

from common.json import ModelEncoder
from .models import Product, Category
from .encoders import ProductEncoder, CategoryEncoder


def send_product_data(product):
    parameters = pika.ConnectionParameters(host="rabbitmq")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange="product_info", exchange_type="fanout")

    message = json.dumps(product, cls=ProductEncoder)
    channel.basic_publish(
        exchange="product_info",
        routing_key="",
        body=message,
    )
    connection.close()

@require_http_methods(["GET", "POST"])
def api_list_products(request):
    if request.method == "GET":
        products = Product.objects.all()
        return JsonResponse(
            {"products": products},
            encoder=ProductEncoder
        )
    else:
        content = json.loads(request.body)
        try:
            category = Category.objects.get(id=content["category"])
            content["category"] = category
        except Category.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid category id"},
                status=400,
            )
        product = Product.objects.create(**content)
        send_product_data(product)
        return JsonResponse(
            product,
            encoder=ProductEncoder,
            safe=False,
        )
@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_product(request, id):
    if request.method == "GET":
        products = Product.objects.get(id=id)
        return JsonResponse(
            {"products": products},
            encoder=ProductEncoder,
        )
    elif request.method == "PUT":
        content = json.loads(request.body)
        try:
            if "category" in content:
                category = Category.objects.get(id=content["category"])
                content["category"] = category
        except Category.DoesNotExist:
               return JsonResponse(
                {"message": "Invalid Category"},
                status=400,
            )
        product = Product.objects.filter(id=id).update(**content)
        product = Product.objects.get(id=id)
        send_product_data(product)
        return JsonResponse(
            product,
            encoder=ProductEncoder,
            safe=False,
        )
    else:
       count, _ = Product.objects.filter(id=id).delete()
       return JsonResponse({"deleted": count > 0})

@require_http_methods(["GET", "POST"])
def api_list_categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return JsonResponse(
            {"categories": categories},
            encoder=CategoryEncoder
        )
    else:
        content = json.loads(request.body)
        try:
            if "parent_category" in content:
                parent_category = Category.objects.get(id=content["parent_category"])
                content["parent_category"] = parent_category
        except Category.DoesNotExist:
               return JsonResponse(
                {"message": "Invalid Category"},
                status=400,
            )
        category = Category.objects.create(**content)
        return JsonResponse(
            category,
            encoder=CategoryEncoder,
            safe=False,
        )

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_category(request, id):
    if request.method == "GET":
        categories = Category.objects.get(id=id)
        return JsonResponse(
            {"categories": categories},
            encoder=CategoryEncoder,
        )
    elif request.method == "PUT":
        content = json.loads(request.body)
        try:
            if "parent_category" in content:
                parent_category = Category.objects.get(id=content["parent_category"])
                content["parent_category"] = parent_category
        except Category.DoesNotExist:
               return JsonResponse(
                {"message": "Invalid Category"},
                status=400,
            )
        category = Category.objects.filter(id=id).update(**content)
        category = Category.objects.get(id=id)
        return JsonResponse(
            category,
            encoder=CategoryEncoder,
            safe=False,
        )
    else:
       count, _ = Category.objects.filter(id=id).delete()
       return JsonResponse({"deleted": count > 0})
