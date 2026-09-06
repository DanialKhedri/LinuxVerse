from django.db import models

from apps.orders.models import Order


class Payment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='payments'
    )

    amount = models.PositiveIntegerField()

    authority = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    ref_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Payment #{self.id} - Order #{self.order.id}'