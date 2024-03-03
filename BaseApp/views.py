from django.shortcuts import render
from .models import Product, Category
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


class ProductListView(TemplateView):
    template_name = 'home/home-page.html'


class ProductFilterView(ListView):
    model = Product
    template_name = 'home/category-search.html'
    queryset = Product.objects.filter(public=True)
    context_object_name = 'products'


class ProductDetailView(DetailView):
    pass


class ProductCreateView(LoginRequiredMixin, CreateView):
    pass


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    pass


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    pass
