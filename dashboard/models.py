from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField('accounts.Account', verbose_name=_(
        "کاربر"), on_delete=models.CASCADE)
    address_line_1 = models.CharField(_(" ادرس تحویل"), max_length=50)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    postal_code = models.CharField(_(" کد پستی"), max_length=50)
    state = models.CharField(_(" استان"), max_length=50)
    city = models.CharField(_("شهر "), max_length=50)
    street = models.CharField(_("خیابان "), max_length=50)
    tag = models.CharField(_(" پلاک"), max_length=50)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1}'

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'


@receiver(post_save, sender='accounts.Account')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
