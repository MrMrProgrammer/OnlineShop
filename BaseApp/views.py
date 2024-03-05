from .models import Product
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(TemplateView):
    template_name = 'home/home-page.html'


class ProductCategoryView(ListView):
    model = Product
    template_name = 'home/category-search.html'
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        self.category = kwargs['category']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.queryset = Product.objects.filter(public=True).filter(category__title__exact=self.category)
        context['products_category'] = self.queryset
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'home/single-product.html'
    context_object_name = 'product'
