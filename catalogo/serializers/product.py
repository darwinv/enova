"""Serializer Producto."""
from rest_framework import serializers
from catalogo.models import Product, ProductDetail, Brand
from rest_framework.response import Response
from rest_framework import status


class ProductDetailValidateSerializer(serializers.ModelSerializer):
    """Serializer para validar detalle."""
    price_offer = serializers.DecimalField(required=False,
                                           max_digits=10, decimal_places=4)
    offer_day_to = serializers.DateTimeField(required=False)
    offer_day_from = serializers.DateTimeField(required=False)

    class Meta:
        model = ProductDetail
        fields = ('is_visible', 'price', 'price_offer', 'offer_day_to',
                  'offer_day_from', 'quantity', 'sku')


class ProductSerializer(serializers.ModelSerializer):
    """Serializer de Producto."""

    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), required=True, allow_null=True)

    class Meta:
        """Modelo Producto y sus campos."""

        model = Product
        fields = ('id', 'name', 'description', 'is_variation', 'type_product',
                  'code', 'family', 'is_active', 'is_complement', 'is_deleted',
                  'created', 'modified', 'brand')

        read_only_fields = ('code',)

    def aument_code(self):
        """Aumentar codigo."""
        new_code = 1
        prod = Product.objects.last()
        if prod:
            new_code = prod.code + 1
        return new_code

    def validate(self, data):
        data_detail = self.context["request"].data
        if self.context["request"].method != 'PUT':
            serializer_detail = ProductDetailValidateSerializer(data=data_detail)
            if serializer_detail.is_valid():
                return data_detail
            return Response(serializer_detail.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return data_detail

    def create(self, validated_data):
        """Redefinido metodo de crear"""
        data_detail = {}
        validated_data['brand'] = Brand.objects.get(pk=validated_data['brand'])
        data_detail['price'] = validated_data.pop('price')
        data_detail['is_visible'] = validated_data.pop('is_visible')
        data_detail['quantity'] = validated_data.pop('quantity')
        data_detail['sku'] = validated_data.pop('sku')
        data_detail['price_offer'] = validated_data.get('price_offer', None)
        data_detail['offer_day_from'] = validated_data.get('offer_day_from', None)
        data_detail['offer_day_to'] = validated_data.get('offer_day_to', None)
        validated_data["code"] = self.aument_code()
        instance = Product.objects.create(**validated_data)
        ProductDetail.objects.create(product=instance, **data_detail)
        return instance

    def update(self, instance, validated_data):
        """Redefinido metodo de actualizar."""
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.type_product = validated_data.get('type_product', instance.type_product)
        instance.family = validated_data.get('family', instance.family)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_variation = validated_data.get('is_variation', instance.is_variation)
        instance.is_complement = validated_data.get('is_complement', instance.is_complement)
        instance.brand = validated_data.get('brand', instance.brand)
        detail = instance.productdetail_set.get()
        detail.price = validated_data.get('price', detail.price)
        detail.is_visible = validated_data.get('is_visible', detail.is_visible)
        detail.quantity = validated_data.get('quantity', detail.quantity)
        detail.price_offer = validated_data.get('price_offer', detail.price_offer)
        detail.offer_day_to = validated_data.get('offer_day_to', detail.offer_day_to)
        detail.offer_day_from = validated_data.get('offer_day_from', detail.offer_day_from)
        detail.save()
        instance.save()
        return instance


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer de Detalle de Producto"""

    class Meta:
        """Modelo."""

        model = Product
        fields = ('id')

    def to_representation(self, obj):
        """Representacion del detalle del producto."""

        detail = obj.productdetail_set.get()

        return {"id": obj.id, "name": obj.name,
                "description": obj.description,
                "price": detail.price,
                "is visible": detail.is_visible,
                "quantity": detail.quantity,
                "price offer": detail.price_offer,
                "offer day from": detail.offer_day_from,
                "offer_day_to": detail.offer_day_to,
                "sku": detail.sku
                }
