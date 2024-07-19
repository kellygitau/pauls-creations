from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# get_object_or_404,redirect

# from item.models import Item

# Create your views here.
@login_required
def index(request):    
    return render (request, 'dashboard/index.html')

def clientbase(request):    
    return render (request, 'dashboard/clients.html')

def products(request):    
    return render (request, 'dashboard/items.html')

def costomer_orders(request):    
    return render (request, 'dashboard/orders.html')

def staff_login(request):    
    return render (request, 'dashboard/staff_login.html')
