from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'address', 'postal_code',
                  'state', 'city', 'street', 'tag']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].label = _("نام و نام خانوادگی")
        self.fields['phone'].label = _(" شماره تماس")
        self.fields['email'].label = _(" ایمیل")
        self.fields['address'].label = _(" ادرس تحویل")
        self.fields['postal_code'].label = _(" کد پستی")
        self.fields['state'].label = _(" استان")
        self.fields['city'].label = _("شهر ")
        self.fields['street'].label = _("خیابان ")
        self.fields['tag'].label = _(" پلاک")
