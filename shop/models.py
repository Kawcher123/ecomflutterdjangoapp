from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    data = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/")
    marcket_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Favorit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isFavorit = models.BooleanField(default=False)

    def __str__(self):
        return f"product Di={self.product.id}|user={self.user.username}|ISFavorite={self.isFavorit}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    isCompile = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User={self.user.username}|ISComplit={self.isCompile}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Qualtity=={self.quantity}"


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=250)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS)
