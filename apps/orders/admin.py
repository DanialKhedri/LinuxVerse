from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'course',
        'amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'name',
        'phone',
        'email',
        'course__title',
    )

    list_display = ('name', 'course', 'purchase_type', 'amount', 'status', 'created_at')
    list_filter = ('purchase_type', 'status')