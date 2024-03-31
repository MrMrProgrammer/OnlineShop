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
