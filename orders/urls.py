from django.urls import path
from .views import PlaceOrderView, PaymentView, OrderCompleteView

app_name = 'order'
urlpatterns = [
    path('place_order/', PlaceOrderView.as_view(), name='place_order_page'),
    path('payments/', PaymentView.as_view(), name='payments_page'),
    path('order_complete/', OrderCompleteView.as_view(),
         name='order_complete_page'),
]
