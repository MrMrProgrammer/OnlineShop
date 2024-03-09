import re
from .models import Product, ProductObject
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(TemplateView):
    template_name = 'home/home-page.html'


class ProductCategoryView(ListView):
    model = ProductObject
    template_name = 'home/category-search.html'

    def get(self, request, *args, **kwargs):
        self.category = kwargs['category_slug']
        self.filtered_by = {}

        pattern = re.compile(r'[^a-zA-Z\s]')
        for k, v in request.GET.lists():
            self.filtered_by[k] = pattern.sub('', str(v))

        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        self.result = ProductObject.objects.filter(available=True, product__category__slug=self.category).order_by('-created')

        for key, value in self.filtered_by.items():
            if key == 'brand':
                self.result = self.result.filter(product__brand__title=value)

        return self.result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_objects'] =self.result
        context['filtered_by'] = self.filtered_by

        return context


class ProductDetailView(DetailView):
    model = ProductObject
    template_name = 'home/single-product.html'
    context_object_name = 'product_object'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        self.all_product_features = {}
        for i in obj.features.all():
            if i.feature_key in self.all_product_features.keys():
                self.all_product_features[i.feature_key].append(i.feature_value)
            else:
                self.all_product_features[i.feature_key] = [i.feature_value]

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_features'] = self.all_product_features
        return context



