from django.apps import AppConfig

class BlogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blogs'  # <-- مهم: مسیر کامل با apps
    verbose_name = 'وبلاگ'