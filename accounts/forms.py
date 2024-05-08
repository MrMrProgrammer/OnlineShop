# from django import forms

# from .models import Account


# class RegistrationForm(forms.ModelForm):
#     username = forms.CharField(max_length=100, required=True)
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'placeholder': 'Enter Password',
#         'class': 'form-control',
#     }))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'placeholder': 'Confirm Password'
#     }))

#     class Meta:
#         model = Account
#         fields = ['username', 'first_name', 'last_name',
#                   'phone_number', 'email', 'password']

#     def clean(self):
#         cleaned_data = super(RegistrationForm, self).clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password != confirm_password:
#             raise forms.ValidationError(
#                 "Password does not match!"
#             )

#     def __init__(self, *args, **kwargs):
#         super(RegistrationForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].widget.attrs['placeholder'] = (
#             'نام را وارد کنید')
#         self.fields['last_name'].widget.attrs['placeholder'] = (
#             'نام خانوادگی را وارد کنید')
#         self.fields['username'].widget.attrs['placeholder'] = (
#             'نام کاربری را وارد کنید')
#         self.fields['phone_number'].widget.attrs['placeholder'] = (
#             'شماره تلفن را وارد کنید')
#         self.fields['email'].widget.attrs['placeholder'] = (
#             'آدرس ایمیل را وارد کن')
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
#-----------------
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ShopUser


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'address', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('phone is exists')
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('phone is exists')
        if not phone.isdigit():
            raise forms.ValidationError('phone must be number')
        if not phone.startswith('09'):
            raise forms.ValidationError('phone must with 09')
        if len(phone) != 11:
            raise forms.ValidationError('phone must be 11')
        return phone


class ShopUserChangeForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'address', 'is_active',
                  'is_staff', 'is_superuser', 'date_join']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('phone is exists')
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('phone is exists')
        if not phone.isdigit():
            raise forms.ValidationError('phone must be number')
        if not phone.startswith('09'):
            raise forms.ValidationError('phone must with 09')
        if len(phone) != 11:
            raise forms.ValidationError('phone must be 11')
        return phone


class LoginForm(forms.Form):
    phone = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
