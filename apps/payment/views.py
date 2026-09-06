from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.orders.models import Order

from .models import Payment
from .services import ZarinpalService


def start_payment(request, access_token):

    order = get_object_or_404(
        Order,
        access_token=access_token
    )

    if order.status == 'paid':
        return redirect(
            'payment:success',
            access_token=order.access_token
        )

    payment = Payment.objects.create(
        order=order,
        amount=order.amount,
        status='pending'
    )

    service = ZarinpalService()

    try:
        result = service.request_payment(payment)

    except Exception:
        payment.status = 'failed'

        payment.save(
            update_fields=['status']
        )

        return redirect(
            'payment:failed',
            access_token=order.access_token
        )

    data = result.get('data', {})

    if data.get('code') != 100:

        payment.status = 'failed'

        payment.save(
            update_fields=['status']
        )

        return redirect(
            'payment:failed',
            access_token=order.access_token
        )

    authority = data.get('authority')

    if not authority:

        payment.status = 'failed'

        payment.save(
            update_fields=['status']
        )

        return redirect(
            'payment:failed',
            access_token=order.access_token
        )

    payment.authority = authority

    payment.save(
        update_fields=['authority']
    )

    return redirect(
        service.payment_url(authority)
    )


def payment_callback(request):

    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if not authority:

        return render(
            request,
            'payment/failed.html',
            {
                'message': 'اطلاعات پرداخت ناقص است.'
            }
        )

    payment = get_object_or_404(
        Payment,
        authority=authority
    )

    if status != 'OK':

        payment.status = 'failed'

        payment.save(
            update_fields=['status']
        )

        return redirect(
            'payment:failed',
            access_token=payment.order.access_token
        )

    if payment.status == 'success':

        return redirect(
            'payment:success',
            access_token=payment.order.access_token
        )

    service = ZarinpalService()

    try:
        result = service.verify_payment(payment)

    except Exception:

        return render(
            request,
            'payment/failed.html',
            {
                'message': (
                    'خطا در ارتباط با درگاه پرداخت. '
                    'لطفاً با پشتیبانی تماس بگیرید.'
                )
            }
        )

    data = result.get('data', {})
    code = data.get('code')

    if code not in [100, 101]:

        payment.status = 'failed'

        payment.save(
            update_fields=['status']
        )

        return redirect(
            'payment:failed',
            access_token=payment.order.access_token
        )

    ref_id = data.get('ref_id')

    with transaction.atomic():

        order = (
            Order.objects
            .select_for_update()
            .get(
                id=payment.order_id
            )
        )

        payment = (
            Payment.objects
            .select_for_update()
            .get(
                id=payment.id
            )
        )

        if payment.status != 'success':

            payment.status = 'success'
            payment.ref_id = ref_id
            payment.paid_at = timezone.now()

            payment.save(
                update_fields=[
                    'status',
                    'ref_id',
                    'paid_at',
                ]
            )

        if order.status != 'paid':

            order.status = 'paid'

            order.save(
                update_fields=['status']
            )

    return redirect(
        'payment:success',
        access_token=order.access_token
    )


def payment_success(request, access_token):

    order = get_object_or_404(
        Order,
        access_token=access_token
    )

    return render(
        request,
        'payment/success.html',
        {
            'order': order
        }
    )


def payment_failed(request, access_token):

    order = get_object_or_404(
        Order,
        access_token=access_token
    )

    return render(
        request,
        'payment/failed.html',
        {
            'order': order,
            'message': (
                'پرداخت انجام نشد یا توسط شما لغو شد.'
            )
        }
    )