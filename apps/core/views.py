from django.shortcuts import render
from apps.courses.models import Course

def home(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'core/home.html', {'courses': courses})