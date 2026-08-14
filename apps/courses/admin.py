from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'original_price',
        'level',
        'is_active',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }



