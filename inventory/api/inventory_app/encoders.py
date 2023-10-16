from common.json import ModelEncoder
from .models import Product, Category

class CategoryEncoder(ModelEncoder):
    model = Category
    properties = [
        "id",
        "name",
        "parent_category",
    ]
    def get_extra_data(self, o):
        extra_data = super().get_extra_data(o)
        if o.parent_category:
            extra_data["parent_category"] = CategoryEncoder().default(o.parent_category)
        return extra_data

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
    encoders = {
        "category": CategoryEncoder(),
    }
