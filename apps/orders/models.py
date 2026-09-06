import uuid

from django.db import models
from apps.courses.models import Course


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    ]
    
    # ===== اضافه کردن این بخش =====
    PURCHASE_TYPE_CHOICES = [
        ('normal', 'معمولی'),
        ('vip', 'VIP'),
    ]
    # ===== پایان بخش اضافه شده =====

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    name = models.CharField(max_length=150)

    phone = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    amount = models.PositiveIntegerField()
    
    # ===== اضافه کردن این فیلد جدید =====
    purchase_type = models.CharField(
        max_length=10,
        choices=PURCHASE_TYPE_CHOICES,
        default='normal',
        help_text="نوع خرید: معمولی یا VIP"
    )
    # ===== پایان فیلد جدید =====

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    access_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.course.title}'