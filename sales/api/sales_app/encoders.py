from common.json import ModelEncoder
from .models import Address, Customer, Order, Status

class CustomerEncoder(ModelEncoder):
    model = Customer
    properties = [
        "id",
        "first_name",
        "last_name",
        "address",
        "phone_number",

    ]


class AddressEncoder(ModelEncoder):
    model = Address
    properties = [
        "id",
        "customer",
        "street_address",
        "apt_number",
        "country",
        "zip_code",
    ]

class OrderEncoder(ModelEncoder):
    model = Order
    properties = [
        'id',
        'customer',
        "product",
        "order_number",
        "status",
    ]


class StatusEncoder(ModelEncoder):
    model = Status
    properties= [
        "id",
        "name",
    ]
