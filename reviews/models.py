from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
from django.urls import reverse


class ReviewStatusType(models.IntegerChoices):
    pending = 1, "در انتظار تایید"
    accepted = 2, "تایید شده"
    rejected = 3, "رد شده"


class Review(models.Model):
    user = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'ProductObject.ProductObject', on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(default=5, validators=[
                               MinValueValidator(0), MaxValueValidator(5)])
    status = models.IntegerField(
        choices=ReviewStatusType.choices,
        default=ReviewStatusType.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.user} - {self.product.id}"

    def get_status(self):
        return {
            "id": self.status,
            "title": ReviewStatusType(self.status).name,
            "label": ReviewStatusType(self.status).label,
        }

    def get_absolute_url(self):
        return reverse('p_objects:detail', args=[self.product.id, ])


@receiver(post_save, sender=Review)
def calculate_avg_review(sender, instance, created, **kwargs):
    if instance.status == ReviewStatusType.accepted.value:
        product = instance.product
        average_rating = Review.objects.filter(
            product=product, status=ReviewStatusType.accepted).aggregate(
                Avg('rate'))['rate__avg']
        product.avg_rate = round(average_rating, 1)
        product.save()
