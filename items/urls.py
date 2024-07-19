from django.urls import path
from .views import *

app_name = 'items'

urlpatterns = [
    path('', items, name='shop'),
    path('checkout/', checkout_view, name='checkout'),
    path('paypal/return/', paypal_return, name='paypal_return'),
    path('paypal/cancel/', paypal_cancel, name='paypal_cancel'),
]