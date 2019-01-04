"""Urls de API Rest."""
from django.conf.urls import url
from catalogo.views import product


urlpatterns = [

    # Productos
    url(r'^products/$', product.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<pk>[0-9]+)/$', product.ProductDetailView.as_view(),
        name='product-detail'),


]
