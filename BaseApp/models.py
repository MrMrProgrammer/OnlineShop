from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from Category.models import Category, Brand, Base


class Image(models.Model):
    image = models.ImageField(_("عکس"), upload_to='images/')

    class Meta:
        verbose_name = _("عکس")
        verbose_name_plural = _("عکس‌ها")


special_features = (
    ('سایز صفحه نمایش', _('صفحه نمایش')),
    ('دوربین', _('دوربین')),
    ('باتری', _('باتری')),
    ('آداپتور', _('شارژر')),
    ('رنگ', _('رنگ')),
    ('رم', _('رم')),
    ('پردازنده', _('پردازنده')),
    ('گرافیک', _('گرافیک')),
    ('حافظه داخلی', _('حافظه داخلی')),
)


class ProductFeature(models.Model):
    feature_key = models.CharField(
        _("مشخصات"), max_length=80, choices=special_features)
    feature_value = models.CharField(_("مقدار"), max_length=250)

    class Meta:
        unique_together = ('feature_key', 'feature_value')
        verbose_name = _("مشخصات")
        verbose_name_plural = _("مشخصات")

    def __str__(self):
        return f'{self.feature_key} - {self.feature_value}'


class Product(Base):
    category = models.ManyToManyField(Category,
                                      verbose_name=_("دسته بندی ها"))
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name='product_brand',
                              verbose_name=_("برند"))
    images = models.ManyToManyField(Image,
                                    verbose_name=_("عکس‌ها"),
                                    blank=True)
    features = models.ManyToManyField('ProductFeature',
                                      verbose_name=_("جزییات"),
                                      related_name='product_features')
    descriptions = models.TextField(
        _('توضیح اجمالی محصول'), max_length=300,
        default='No description provided')
    public = models.BooleanField(_("نمایش عمومی"), default=False)

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")

    def __str__(self):
        return self.title

    def get_url(self):
        if self.category.exists():
            return reverse('home-page', args=[self.category.first().slug, self.slug])
        return reverse('home-page', args=[self.slug])
#--------------------------------------------------new 5/15
from django.db import models
from shop.models import Product


# Create your models here.


class ProductFeature(models.Model):
    feature_key = models.CharField(max_length=80)
    feature_value = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_features')

    class Meta:
        unique_together = ('feature_key', 'feature_value')
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی'

    def __str__(self):
        return f'{self.feature_key} : {self.feature_value}'


class Image(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True),
    file = models.ImageField(upload_to='product_image/%Y/%m/%d'),
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='تصویرها'),
    description = models.TextField(max_length=2000, null=True, blank=True),
    create = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['-create'])
        ]

    def __str__(self):
        return self.title if self.title else 'None'

