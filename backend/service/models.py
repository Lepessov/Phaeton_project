from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class SalesData(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients')
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='products')
    transaction_date = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=0)


class SearchHistory(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='customers')
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='goods', default=1)
    search_query = models.CharField(max_length=100)
    search_date = models.DateTimeField()
    city = models.CharField(max_length=100)


