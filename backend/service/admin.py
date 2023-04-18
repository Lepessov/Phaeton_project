from django.contrib import admin
from .models import (Products, SalesData, SearchHistory, Client)

# Register your models here.

admin.site.register(Products)
admin.site.register(SearchHistory)
admin.site.register(SalesData)
admin.site.register(Client)