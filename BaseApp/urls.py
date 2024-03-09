from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home-page'),
    path('category/<slug:category_slug>/', views.ProductCategoryView.as_view(), name='filter'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='detail'),

]
