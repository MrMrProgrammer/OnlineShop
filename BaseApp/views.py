import re
from .models import Product, Objects
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(TemplateView):
    template_name = 'home/home-page.html'


class ProductCategoryView(ListView):
    model = Objects
    template_name = 'home/category-search.html'

    def get(self, request, *args, **kwargs):
        self.category = kwargs['category_id']
        self.filtered_by = {}

        pattern = re.compile(r'[^a-zA-Z\s]')
        for k, v in request.GET.lists():
            self.filtered_by[k] = pattern.sub('', str(v))

        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        self.result = Options.objects.filter(available=True).order_by('-created')

        for key, value in self.filtered_by.items():
            if key == 'brand':
                self.result = self.result.filter(product__brand__title=value)

            # if key == 'exist' and value == 'True': self.queryset.filter(stock__gte=1)
            # if key == 'by_popular': self.queryset.filter(recomended__range=6)

        return self.result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['objects'] =self.result
        context['filtered_by'] = self.filtered_by

        return context


class ProductDetailView(DetailView):
    model = Objects
    template_name = 'home/single-product.html'
    context_object_name = 'object'

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



