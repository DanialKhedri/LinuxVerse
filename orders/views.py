from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course
from .forms import OrderForm
from .models import Order


def create_order(request, slug):
    course = get_object_or_404(
        Course,
        slug=slug,
        is_active=True
    )

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            order.course = course
            order.amount = course.price
            order.status = 'pending'

            order.save()

            return redirect(
                'order_success',
                access_token=order.access_token
            )

    else:
        form = OrderForm()

    return render(
        request,
        'orders/order.html',
        {
            'course': course,
            'form': form,
        }
    )


def order_success(request, access_token):
    order = get_object_or_404(
        Order,
        access_token=access_token
    )

    return render(
        request,
        'orders/order_success.html',
        {
            'order': order
        }
    )