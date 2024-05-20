from django.urls import path
from .views import (
    AddToCartView,
    CartView, RemoveCartView, DeleteCartItemView,
    CheckoutView)

app_name = 'cart'
urlpatterns = [
    path('cart_page/', CartView.as_view(), name='cart_page'),
    path('add/<int:product_id>/', AddToCartView.as_view(),
         name='add_to_cart_page'),
    path('remove_from_cart/<int:product_id>/<int:cart_item_id>/',
         RemoveCartView.as_view(), name='remove_from_cart_page'),
    path('delete_cart_item/<int:product_id>/<int:cart_item_id>/',
         DeleteCartItemView.as_view(), name='delete_cart_item_page'),

    path('checkout/', CheckoutView.as_view(), name='checkout_page')
]
#----------------------new 17/5
from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('cart-detail', cart_detail, name='cart-detail'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('decrease/<int:product_id>/', decrease_from_cart, name='decrease_from_cart'),
    path('item_remove/<int:product_id>/', remove_item, name='item_remove'),
    path('cart-detail', cart_detail, name='update_quantity'),
]
