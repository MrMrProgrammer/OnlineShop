from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home-page'),
    path('category/<str:category>/', views.ProductCategoryView.as_view(), name='filter'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='detail'),

]
