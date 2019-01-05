from catalogo.serializers.product import ProductSerializer
from catalogo.serializers.product import ProductDetailSerializer
from catalogo.serializers.product import ProductDetailValidateSerializer
from rest_framework.generics import ListCreateAPIView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from catalogo.models import Product
from rest_framework import status, permissions
from django.http import Http404
from django.shortcuts import get_object_or_404
# Create your views here.


class ProductListView(ListCreateAPIView):
    """Listar Productos."""
    authentication_classes = (OAuth2Authentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.filter(is_deleted=False).order_by("-id")

    def list(self, request):
        """Listar Productos"""
        products = Product.objects.filter(is_deleted=False).order_by("-id")
        # paginacion

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(products, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        """Crear producto"""
        data = request.data
        serializer = ProductSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """Detalle"""
    authentication_classes = (OAuth2Authentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data,
                                       context={'request': request},
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_deleted = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
