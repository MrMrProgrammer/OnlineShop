from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist

from BaseApp.models import Product, ProductFeature

from .models import Cart, CartItem

# Create your views here.


# private function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


class AddToCartView(LoginRequiredMixin, View):
    def get_cart(self, request):
        try:
            return Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Cart.objects.create(user=request.user)

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart(request)
        product_feature = []

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if created:
            cart_item.product_object_id = product.productobject_set
        else:
            cart_item.product_object_id = product.productobject_set

        # بررسی می‌کنیم که آیا فیلد `product_feature` در درخواست وجود دارد
        if 'product_feature' in request.POST:
            product_feature = ProductFeature.objects.filter(
                id__in=request.POST.getlist('product_feature'))
            cart_item.product_feature.set(product_feature)

        cart_item.save()
        return redirect('cart:cart_page')


class RemoveCartView(LoginRequiredMixin, View):
    def get(self, request, product_id, cart_item_id):
        product = get_object_or_404(Product, id=product_id)
        try:
            if request.user.is_authenticated:
                # ابتدا سبد خرید (cart) مربوط به کاربر را پیدا می‌کنیم
                cart = Cart.objects.get(user=request.user)
                # حالا می‌توانیم CartItem را بر اساس cart و id پیدا کنیم
                cart_item = CartItem.objects.get(
                    product=product, cart=cart, id=cart_item_id)
            else:
                # cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(
                    product=product, cart=cart, id=cart_item_id)

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except Cart.DoesNotExist:
            pass
        except CartItem.DoesNotExist:
            pass  # اگر CartItem وجود نداشت، اینجا چیزی انجام ندهید
        return redirect('cart:cart_page')


class DeleteCartItemView(LoginRequiredMixin, View):
    def get(self, request, product_id, cart_item_id):
        # product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, id=cart_item_id)
        cart_item.delete()
        return redirect('cart:cart_page')

    def get_cart(self, request):
        try:
            return Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Cart.objects.create(user=request.user)


class CartView(View):
    def get(self, request):
        cart_items = []
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart)
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id).first()
                if cart:
                    cart_items = CartItem.objects.filter(cart=cart)

        total = 0
        tax = 0
        grand_total = 0
        total_quantity = 0
        if cart_items:
            for cart_item in cart_items:
                total += sum(item.product_object.all().count()
                             for item in [cart_item])
            tax = 0.02 * total
            grand_total = total + tax
            total_quantity = total

        context = {
            'total': total,
            'quantity': total_quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'carts/cart.html', context)


class CheckoutView(LoginRequiredMixin, View):
    login_url = 'account:login_page'  # این جایگزین دکوراتور login_required می‌شود

    def get(self, request):
        total = 0
        quantity = 0
        cart_items = []
        tax = 0
        grand_total = 0

        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(cart__user=request.user)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)

            for cart_item in cart_items:
                total += cart_item.sub_total  # استفاده از متد sub_total
                quantity += cart_item.quantity

            tax = (2 * total) / 100
            grand_total = total + tax

        except ObjectDoesNotExist:
            pass

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
        }

        return render(request, 'carts/checkout.html', context)
