from django.urls import path
from core.views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('products/', products, name='products'),
    path('order/', order, name='order'),
    path('gallery/', gallery, name='gallery'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('submit_form/', submit_form, name='submit_form'),
]
