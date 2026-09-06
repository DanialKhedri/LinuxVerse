from django.urls import path

from . import views


app_name = 'payment'


urlpatterns = [

    path(
        'start/<uuid:access_token>/',
        views.start_payment,
        name='start'
    ),

    path(
        'callback/',
        views.payment_callback,
        name='callback'
    ),

    path(
        'success/<uuid:access_token>/',
        views.payment_success,
        name='success'
    ),

    path(
        'failed/<uuid:access_token>/',
        views.payment_failed,
        name='failed'
    ),

]