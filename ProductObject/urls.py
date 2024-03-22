from django.urls import path

from .views import ProductCategoryView

urlpatterns = [

    path('<slug:category_slug>/',
         ProductCategoryView.as_view(), name='filter'),
]
