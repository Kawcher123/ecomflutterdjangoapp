from django.contrib import admin
from .models import Category, Product, Favorit, CartProduct, Order, Cart


admin.site.register([Category, Product, Favorit, CartProduct, Order, Cart])
