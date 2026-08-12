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
                order_id=order.id
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


def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        'orders/order_success.html',
        {
            'order': order
        }
    )