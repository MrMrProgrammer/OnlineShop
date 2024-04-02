from django.urls import path

from .views import (change_password,
                    edit_profile, profile,
                    MyOrdersView, OrderDetailView)

app_name = 'dashboard'
urlpatterns = [
    path('profile/', profile, name=("profile_page")),

    path('edit_profile/', edit_profile, name='edit_profile_page'),
    path('change_password/', change_password, name='change_password_page'),
    path('my_orders/', MyOrdersView.as_view(), name='my_orders_page'),
    path('order_detail/<int:order_id>/',
         OrderDetailView.as_view(), name='order_detail_page'),


]
