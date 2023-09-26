from common.json import ModelEncoder
from .models import Address, Customer

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
