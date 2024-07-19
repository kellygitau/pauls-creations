from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('clientbase/', views.clientbase, name="clentbase"),
    path('products/', views.products, name="products"),
    path('orders/', views.costomer_orders, name="orders"),
    path('staff_login/', views.staff_login, name='staff_login'),
]