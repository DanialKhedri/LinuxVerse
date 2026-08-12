from django.shortcuts import get_object_or_404, redirect, render

from .models import Course

def course_detail(request, slug):
    course = get_object_or_404(
        Course,
        slug=slug,
        is_active=True
    )

    return render(
        request,
        'courses/course_detail.html',
        {'course': course}
    )

