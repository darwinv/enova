"""Modelos de la Api."""
from django.db import models
# Create your models here.


class Brand(models.Model):
    """Brand o Marca"""
    name = models.CharField(max_length=150)


class Product(models.Model):
    """Producto."""

    name = models.CharField(max_length=150)
    description = models.TextField()
    type_product = models.CharField(max_length=3)
    code = models.PositiveIntegerField()
    family = models.PositiveIntegerField(default=1)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_variation = models.BooleanField(default=False)
    is_complement = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

    def __str__(self):
        """nombre."""
        return self.name


class ProductDetail(models.Model):
    """Detalle de Producto."""

    is_visible = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_offer = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=True)
    offer_day_from = models.DateTimeField(null=True)
    offer_day_to = models.DateTimeField(null=True)
    quantity = models.PositiveIntegerField()
    sku = models.CharField(max_length=4, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
