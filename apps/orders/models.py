import uuid

from django.db import models
from apps.courses.models import Course


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    name = models.CharField(max_length=150)

    phone = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    amount = models.PositiveIntegerField()

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