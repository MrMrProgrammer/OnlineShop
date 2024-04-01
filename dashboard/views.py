from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from accounts.models import Account
from orders.models import Order, OrderProduct

from .models import UserProfile
from .forms import UserForm, UserProfileForm

# Create your views here.


@login_required(login_url='account:login_page')
def profile(request):
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        userprofile = None

    context = {
        'userprofile': userprofile,
    }
    return render(request, 'dashboard/profile.html', context)


@login_required(login_url='account:login_page')
def edit_profile(request):
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '🎉 مشخصات شما به روز شده است.')
            return redirect('dashboard:edit_profile_page')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'dashboard/edit_profile.html', context)


@login_required(login_url='account:login_page')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'رمز عبور با موفقیت به روز شد.')
                return redirect('dashboard:change_password_page')
            else:
                messages.error(
                    request, 'لطفا رمز عبور فعلی معتبر را وارد کنید')
                return redirect('dashboard:change_password_page')
        else:
            messages.error(request, 'رمز عبور مطابقت ندارد!')
            return redirect('dashboard:change_password_page')
    return render(request, 'dashboard/change_password.html')


class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'dashboard/my_orders.html'
    context_object_name = 'orders'
    login_url = 'account:login_page'

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user, is_ordered=True).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'
    login_url = 'account:login_page'
    pk_url_kwarg = 'order_id'

    def get_object(self, queryset=None):
        order_id = self.kwargs.get(self.pk_url_kwarg)
        order = get_object_or_404(self.model, order_number=order_id)
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context['order']
        order_detail = OrderProduct.objects.filter(order=order)
        subtotal = sum(item.product_price *
                       item.quantity for item in order_detail)

        context.update({
            'order_detail': order_detail,
            'subtotal': subtotal,
        })
        return context
