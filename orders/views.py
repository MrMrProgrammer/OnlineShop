from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect, get_object_or_404

from carts.models import CartItem, Cart

from .forms import OrderForm
from .models import Order, Payment, OrderProduct

# Create your views here.


class PaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    fields = ['payment_id', 'payment_method', 'amount_paid', 'status']

    def form_valid(self, form):
        form.instance.user = self.request.user
        order = get_object_or_404(Order, user=self.request.user,
                                  is_ordered=False,
                                  order_number=self.request.POST['orderID'])
        form.instance.order = order
        order.is_ordered = True
        order.save()
        self.move_cart_items_to_order(order)
        self.send_order_received_email(order)
        data = {
            'order_number': order.order_number,
            'transID': form.instance.payment_id,
        }
        return JsonResponse(data)

    def move_cart_items_to_order(self, order):
        cart_items = CartItem.objects.filter(user=self.request.user)
        for item in cart_items:
            orderproduct = OrderProduct.objects.create(
                order=order,
                payment=self.object,
                user=self.request.user,
                product=item.product,
                quantity=item.quantity,
                variations=item.variations,
                product_price=item.product.price,
                ordered=True
            )
            orderproduct.variations.set(item.variations.all())
            item.product.stock -= item.quantity
            item.product.save()
        cart_items.delete()

    def send_order_received_email(self, order):
        mail_subject = 'ممنون ک مارو برا خریدتون انتخاب کردین.'
        message = render_to_string(
            'orderes/ordered_recieved_email.html',
            {
                'user': self.request.user,
                'order': order,
            })
        to_email = self.request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()


class PlaceOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/payments.html'


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['quantity'] = 0  # افزودن مقدار اولیه برای 'quantity'
    cart = Cart.objects.filter(user=self.request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total_price_for_item = sum(
            [po.price for po in cart_item.product_object.all()])
        grand_total += (total_price_for_item * cart_item.quantity)
        context['quantity'] += cart_item.quantity
    tax = (2 * grand_total) / 100
    grand_total += tax
    context.update({
        'cart_items': cart_items,
        'total': grand_total - tax,
        'tax': tax,
        'grand_total': grand_total,
    })
    return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.order_total = self.context['grand_total']
        form.instance.tax = self.context['tax']
        form.instance.ip = self.request.META.get('REMOTE_ADDR')
        form.instance.order_number = self.generate_order_number()
        return super().form_valid(form)

    def generate_order_number(self):
        current_date = now().strftime('%Y%m%d')
        return f"{current_date}{self.object.id}"

    def get_success_url(self):
        return redirect('orders:payment', pk=self.object.pk)


class OrderCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, order_number=self.request.GET.get(
            'order_number'), is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order=order)
        subtotal = 0
        for product in ordered_products:
            subtotal += product.product_price * product.quantity
        payment = get_object_or_404(
            Payment, payment_id=self.request.GET.get('payment_id'))
        context.update({
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        })
        return context
