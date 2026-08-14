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

    price = models.PositiveIntegerField()
    original_price = models.PositiveIntegerField()

    duration = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


