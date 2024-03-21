from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Base(models.Model):
    title = models.CharField(_("عنوان"), max_length=50,
                             blank=True, unique=True)
    slug = models.SlugField(_("ادرس"), unique=True, max_length=100)
    image = models.ImageField(_("عکس کاور"),
                              upload_to='images/',
                              height_field=None,
                              width_field=None, max_length=None)

    class Meta:
        abstract = True


class Brand(Base):

    class Meta:
        verbose_name = _("برند")
        verbose_name_plural = _("برند ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])

#  _______      _____________


class Category(Base):
    parent = models.ForeignKey('self',
                               default=None,
                               null=True,
                               blank=True,
                               verbose_name=_("دسته بندی"),
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])
