from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    image = models.ImageField(
        upload_to='courses/',
        blank=True,
        null=True
    )

    description = CKEditor5Field(
        'Description',
        config_name='extends'
    )

    # ===== تغییرات اینجا شروع میشه =====
    # قیمت معمولی (همون قیمت قبلی)
    price = models.PositiveIntegerField()
    
    # قیمت VIP (جدید)
    price_vip = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="قیمت VIP - اگر خالی بذاری، VIP برای این دوره غیرفعال میشه"
    )
    
    # قیمت اصلی برای تخفیف‌ها (همون قبلی)
    original_price = models.PositiveIntegerField()
    
    # آیا این دوره گزینه VIP داره؟ (جدید)
    has_vip = models.BooleanField(
        default=False,
        help_text="اگر True باشه، گزینه VIP برای این دوره فعال میشه"
    )
    # ===== تغییرات اینجا تموم میشه =====

    duration = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title