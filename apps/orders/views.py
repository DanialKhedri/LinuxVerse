from django.shortcuts import get_object_or_404, redirect, render

from apps.courses.models import Course
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

            # ===== این بخش مهمه =====
            # دریافت نوع خرید از فرم
            purchase_type = request.POST.get('purchase_type', 'normal')
            
            # تعیین قیمت بر اساس نوع خرید
            if purchase_type == 'vip' and course.has_vip and course.price_vip:
                amount = course.price_vip
            else:
                amount = course.price
                purchase_type = 'normal'
            # ===== ============= =====

            order.course = course
            order.amount = amount  # اینجا باید قیمت VIP باشه
            order.purchase_type = purchase_type
            order.status = 'pending'

            order.save()

            return redirect(
                'payment:start',
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