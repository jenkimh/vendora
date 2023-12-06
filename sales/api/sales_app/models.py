from django.db import models
from django.urls import reverse


class ProductVO(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.CharField(max_length=200)
    image = models.ImageField()
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Address(models.Model):
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="addresses"
    )
    street_address = models.CharField(max_length=100)
    apt_number = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return f"Address for {self.customer.first_name} {self.customer.last_name}"


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.ForeignKey(
        Address, related_name="address", on_delete=models.CASCADE, null=True, blank=True
    )
    phone_number = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_api_url(self):
        return reverse("api_customer", kwargs={"pk": self.id})


class Status(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "statuses"


class Payment(models.Model):
    pass


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer"
    )
    product = models.ForeignKey(ProductVO, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=15)
    ordered_date = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default="PENDING")
    shipping_address = models.ForeignKey(
        Address, related_name="shipping_address", on_delete=models.CASCADE
    )
    billing_address = models.ForeignKey(
        Address, related_name="billing_address", on_delete=models.CASCADE
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, blank=True, null=True
    )

    def ship(self):
        status = Status.objects.get(name="SHIPPED")
        self.status = status
        self.save()

    def deliver(self):
        status = Status.objects.get(name="DELIVERED")
        self.status = status
        self.save()

    def get_api_url(self):
        return reverse("api_order", kwargs={"id": self.id})

    def __str__(self):
        return self.customer


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def calculate_subtotal(self):
        subtotal = sum(
            order_product.product.price for order_product in self.order_products.all()
        )
        return subtotal

    def save(self, *args, **kwargs):
        self.subtotal = self.calculate_subtotal()
        super().save(*args, **kwargs)

    def add_product(self, product):
        OrderProduct.objects.create(cart=self, product=product)

    def remove_product(self, product):
        try:
            order_product = self.order_products.get(product=product)
            order_product.delete()
        except OrderProduct.DoesNotExist:
            pass


class OrderProduct(models.Model):
    product = models.ForeignKey(ProductVO, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="add_to_cart", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.product

    def subtotal(self):
        return self.product.price
