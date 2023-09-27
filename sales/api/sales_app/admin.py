from django.contrib import admin
from .models import Customer, Address, Order, Status, Cart, OrderProduct
# Register your models here.

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Status)
admin.site.register(Cart)
admin.site.register(OrderProduct)
