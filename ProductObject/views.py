from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import ProductObject, Wishlist
from reviews.models import Review
from django.db.models import Q, Avg
from reviews.forms import SubmitReviewForm


class ProductCategoryView(ListView):
    model = ProductObject
    template_name = 'home/category-search.html'
    paginate_by = 2

    # def get_paginate_by(self, queryset):
    #     return self.request.GET.get('page-size', self.paginate_by)

    def get(self, request, *args, **kwargs):

        self.slug = kwargs['category_slug'] or None
        self.filtered_by = {}

        for k, v in request.GET.lists():
            self.filtered_by[k] = v

        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        """
        filter items by category & custom filters & keyword
        :return: Product objects
        """

        # check if user choose a category
        if self.slug != 'search-result':
            self.filter_result = ProductObject.objects.filter(
                available=True,
                product__category__slug=self.slug)
        else:
            self.filter_result = ProductObject.objects.filter(available=True)

        for key, value in self.filtered_by.items():
            if key == 'keyword' and value[0]:
                self.filter_result = self.filter_result.filter(Q(
                    product__title__icontains=value[0]) |
                    Q(description__icontains=value[0]))

            if key == 'brand' and value[0]:
                self.filter_result = self.filter_result.filter(
                    product__brand__title__in=value)

            if key == 'price-gte' and value[0]:
                self.filter_result = self.filter_result.filter(
                    price__gte=value[0] or 0)
            if key == 'price-lte' and value[0]:
                self.filter_result = self.filter_result.filter(
                    price__lte=value[0] or 0)

            if key == 'color' and value[0]:
                self.filter_result = self.filter_result.filter(
                    features__feature_value__in=value)

            if key == 'stock' and value[0]:
                if value[0] == 'true':
                    self.filter_result = self.filter_result.filter(
                        stock__gte=1)
                else:
                    self.filter_result = self.filter_result.filter(
                        stock__lte=0)

            if key == 'order-by' and value[0]:
                if value[0] == 'most-rate':
                    self.filter_result = self.filter_result.filter(
                        avg_rate__gte=3.7)
                if value[0] == 'most-sold':
                    avg_sold = self.filter_result.aggregate(
                        avg_sold=Avg('sold'))['avg_sold']
                    self.filter_result = self.filter_result.filter(
                        sold__gte=avg_sold)

        return self.filter_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_objects'] = self.filter_result.order_by('-created')

        return context


class ProductDetailView(DetailView, CreateView):
    model = ProductObject
    form_class = SubmitReviewForm
    template_name = 'home/single-product.html'
    context_object_name = 'product_object'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        self.all_product_features = {}
        for i in obj.features.all():
            if i.feature_key in self.all_product_features.keys():
                self.all_product_features[i.feature_key].append(
                    i.feature_value)
            else:
                self.all_product_features[i.feature_key] = [i.feature_value]

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(
            product__id=self.get_object().id).filter(status=2).order_by(
                '-created_date')

        context['product_features'] = self.all_product_features
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.get_object()
        form.save()

        return super().form_valid(form)


class AddOrRemoveWishlistView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs['pk']
        print(product_id)
        message = ""
        if product_id:
            try:
                wishlist_item = Wishlist.objects.get(
                    product__id=product_id, user=request.user)
                wishlist_item.delete()
                message = "محصول از لیست علایق حذف شد"
                return JsonResponse({"message": message})

            except Wishlist.DoesNotExist:
                Wishlist.objects.create(
                    product_id=product_id, user=request.user)
                message = "محصول به لیست علایق اضافه شد"
        return JsonResponse({"message": message})
