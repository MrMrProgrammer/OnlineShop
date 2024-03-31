from django import forms
from .models import Review
from ProductObject.models import ProductObject

class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rate', 'description']
        error_messages = {
            'description': {
                'required': 'فیلد توضیحات اجباری است',
            },
        }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     product = cleaned_data.get('product')

    #     try:
    #         # فقط یوزر هایی که محصول رو خریدن 
    #         # چک کنه توی سفارشات بوده یا نه

    #         ProductObject.objects.get(id=product.id, available=True)
    #     except ProductObject.DoesNotExist:
    #         raise forms.ValidationError("این محصول وجود ندارد")

    #     return cleaned_data
    