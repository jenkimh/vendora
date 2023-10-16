from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_api_url(self):
        return reverse("api_category", kwargs={"pk": self.id})

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.CharField(max_length=200)
    image = models.URLField(blank= True, null= True)
    category= models.ForeignKey(Category, related_name="items",
                                on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def get_api_url(self):
        return reverse("api_product", kwargs={"pk": self.id})
