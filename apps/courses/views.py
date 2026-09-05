from django.shortcuts import get_object_or_404, redirect, render

from apps.courses.models import Course

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

def courses(request):  
    all_courses = Course.objects.all().order_by('-created_at')       
    return render(request, 'courses/courses.html', {'courses': all_courses})