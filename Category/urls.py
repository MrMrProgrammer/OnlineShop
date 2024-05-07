from django.urls import path
from .views import (BrandView,)

app_name = 'category'
urlpatterns = [
    path('brands/<slug:slug>/', BrandView.as_view(),
         name='brand_detail'),
]
