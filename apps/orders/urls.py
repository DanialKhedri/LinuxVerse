from django.urls import path

from . import views


urlpatterns = [
    path(
        'courses/<slug:slug>/buy/',
        views.create_order,
        name='create_order'
    ),

   path(
    'order/<uuid:access_token>/success/',
    views.order_success,
    name='order_success'
),
]