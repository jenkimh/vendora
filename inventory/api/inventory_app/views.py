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

# def create_product(json_content):
#     try:
#         content = json.loads(json_content)
#     except json.JSONDecodeError:
#         return 400, {"message": "Bad JSON"}, None

#     required_properties = [
#         "title",
#         "price",
#         "description",
#         "image",
#         "category",
#     ]
#     missing_properties = []
#     for required_property in required_properties:
#         if (
#             required_property not in content
#             # or len(content[required_property]) == 0
#         ):
#             missing_properties.append(required_property)
#     if missing_properties:
#         response_content = {
#             "message": "missing properties",
#             "properties": missing_properties,
#         }
#         return 400, response_content, None
#     try:
#         product = Product.objects.create_product(
#             title=content["title"],
#             price=content["price"],
#             description=content["description"],
#             image=content["image"],
#             category=content["category"],
#         )
#         return 200, product, product
#     except IntegrityError as e:
#         return 409, {"message": str(e)}, None
#     except ValueError as e:
#         return 400, {"message": str(e)}, None


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

        # send_product_data(product)
        return JsonResponse(
            product,
            encoder=ProductEncoder,
            safe=False,
        )
        # status_code, response_content = create_product(request.body)
        # if status_code >= 200 and status_code < 300:
        # response = JsonResponse(
        #     response_content,
        #     encoder=ProductEncoder,
        #     safe=False,
        # )
        # response.status_code = status_code
        # return response


@require_http_methods(["GET", "PUT", "DELETE"])
def api_product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        print("User.DoesNotExist", id)
        if request.method == "GET":
            response = JsonResponse({"message": id})
            response.status_code = 404
            return response
        else:
            product = None

    if request.method == "GET":
        return JsonResponse(
            product,
            encoder=ProductEncoder,
            safe=False,
        )
    elif request.method == "PUT":
        try:
            content = json.loads(request.body)
        except json.JSONDecodeError:
            response = JsonResponse({"message": "Bad JSON"})
            response.status_code = 400
            return response

        if product is not None:
            product.objects.filter(id=id).update(**content)
            product = Product.objects.get(id=id)
            status = 200
            response_content = product
        else:
            status, response_content, product = create_product(request.body)
        if product:
            product.save()
            send_product_data(product)
        response = JsonResponse(
            response_content,
            encoder=ProductEncoder,
            safe=False,
        )
        response.status_code = status
        return response
    else:
        product = Product.objects.filter(id=id).delete()
        send_product_data(product)
        response = HttpResponse()
        response.status_code = 204
        return response

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
        category = Category.objects.create(**content)
        return JsonResponse(
            category,
            encoder=CategoryEncoder,
            safe=False,
        )
