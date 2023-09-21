from common.json import ModelEncoder
from .models import Product, Category

class ProductEncoder(ModelEncoder):
    model = Product
    properties = [
        "id",
        "title",
        "price",
        "description",
        "image",
        "category",
    ]


class CategoryEncoder(ModelEncoder):
    model = Category
    properties = [
        "id",
        "name",
        "parent_category",
    ]
