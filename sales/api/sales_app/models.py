from django.db import models
from django.urls import reverse

# Create your models here.
class Address(models.Model):
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='addresses'
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
        Address,
        related_name="address",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    phone_number = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_api_url(self):
        return reverse("api_customer", kwargs={"pk": self.id})

#might encounter circular import issues since
#address and customer have two way relationship
