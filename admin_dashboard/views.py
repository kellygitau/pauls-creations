from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from admin_dashboard.models import *
from admin_dashboard.services import place_order
from core.forms import LoginForm, signupForm
from items.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from background_task import background
from django.utils import timezone

from admin_dashboard.forms import *

from google_auth_oauthlib.flow import Flow


def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_staff, login_url='admin_login/')(view_func))
    return decorated_view_func

@admin_required
def index(request):
    orders = Ordering.objects.filter(is_paid=False)[0:10]
    
    products = Product.objects.all()
    # Check to see if logging in
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:    
        return render(request, 'admin_dashboard/index.html', {'products':products,'orders':orders,})

# def signup(request):
#     if request.method == 'POST':
#         form = signupForm(request.POST)
        
#         if form.is_valid():
#             form.save()
            
#             return redirect('/')
    
#     else:
#         form = signupForm()
    
#     return render(request, 'core/signup.html', {
#         'form':form
#     })
    
# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
        
#         if form.is_valid():
#             form.save()
            
#             return redirect('core')
    
#     else:
#         form = LoginForm()
        
#     return render(request, 'core/login.html', {
#         'form':form
#     })
  
def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

@admin_required
def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, prefix='category')
        if category_form.is_valid():
            category_form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Category created successfully.'})
            messages.success(request, 'Category created successfully.')
            return redirect('admin_dashboard:tables')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': category_form.errors})
            messages.error(request, 'Error creating category. Please correct the errors below.')
    else:
        category_form = CategoryForm(prefix='category')

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin_dashboard/admin_forms.html', {'category_form': category_form})

@admin_required
def add_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST, prefix='item')
        if item_form.is_valid():
            item_form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Item created successfully.'})
            messages.success(request, 'Item created successfully.')
            return redirect('admin_dashboard:tables')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': item_form.errors})
            messages.error(request, 'Error creating item. Please correct the errors below.')
    else:
        item_form = ItemForm(prefix='item')

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin_dashboard/admin_forms.html', {'item_form': item_form})

@admin_required
def add_product(request):
    if request.method == 'POST':
        product_form = NewItemForm(request.POST, request.FILES, prefix='product')
        if product_form.is_valid():
            product_form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Product created successfully.'})
            messages.success(request, 'Product created successfully.')
            return redirect('admin_dashboard:tables')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': product_form.errors})
            messages.error(request, 'Error creating product. Please correct the errors below.')
    else:
        product_form = NewItemForm(prefix='product')

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin_dashboard/admin_forms.html', {'product_form': product_form})

@admin_required
def add_material(request):
    if request.method == 'POST':
        material_form = MaterialForm(request.POST, prefix='material')
        if material_form.is_valid():
            material_form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Material created successfully.'})
            messages.success(request, 'Material created successfully.')
            return redirect('admin_dashboard:tables')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': material_form.errors})
            messages.error(request, 'Error creating material. Please correct the errors below.')
    else:
        material_form = MaterialForm(prefix='material')

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin_dashboard/admin_forms.html', {'material_form': material_form})

@admin_required
def add_material_size(request):
    if request.method == 'POST':
        material_size_form = MaterialSizeForm(request.POST, prefix='material_size')
        if material_size_form.is_valid():
            material_size_form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Material size created successfully.'})
            messages.success(request, 'Material size created successfully.')
            return redirect('admin_dashboard:tables')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': material_size_form.errors})
            messages.error(request, 'Error creating material size. Please correct the errors below.')
    else:
        material_size_form = MaterialSizeForm(prefix='material_size')

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin_dashboard/admin_forms.html', {'material_size_form': material_size_form})

@admin_required
def add_paper_size(request):
    if request.method == 'POST':
        paper_size_form = PaperSizeForm(request.POST, request.FILES, prefix='paper_size')
        if paper_size_form.is_valid():
            paper_size_form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Paper size created successfully.'})
            messages.success(request, 'Paper size created successfully.')
            return redirect('admin_dashboard:tables')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': paper_size_form.errors})
            messages.error(request, 'Error creating paper size. Please correct the errors below.')
    else:
        paper_size_form = PaperSizeForm(prefix='paper_size')

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin_dashboard/admin_forms.html', {'paper_size_form': paper_size_form})

@admin_required
def add_vendor(request):
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, prefix='vendor')
        if vendor_form.is_valid():
            vendor_form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Vendor created successfully.'})
            messages.success(request, 'Vendor created successfully.')
            return redirect('admin_dashboard:tables')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': vendor_form.errors})
            messages.error(request, 'Error creating vendor. Please correct the errors below.')
    else:
        vendor_form = VendorForm(prefix='vendor')

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin_dashboard/admin_forms.html', {'vendor_form': vendor_form})
@admin_required
def admin_forms(request):
    category_form = CategoryForm(prefix='category')
    item_form = ItemForm(prefix='item')
    product_form = NewItemForm(prefix='product')
    material_form = MaterialForm(prefix='material')
    material_size_form = MaterialSizeForm(prefix='material_size')
    paper_size_form = PaperSizeForm(prefix='paper_size')
    vendor_form = VendorForm(prefix='vendor')

    context = {
        'category_form': category_form,
        'item_form': item_form,
        'product_form': product_form,
        'material_form': material_form,
        'material_size_form': material_size_form,
        'paper_size_form': paper_size_form,
        'vendor_form': vendor_form,
    }
    return render(request, 'admin_dashboard/admin_forms.html', context)

def tables(request):
    query = request.GET.get('query', '').strip()
    categories = Category.objects.all()
    products = Product.objects.all()
    items = Item.objects.all()
    vendor_list = Vendors.objects.all()
    items_per_page = 10

    if query:
        items = items.filter(
            Q(name__icontains=query)
        )
        vendor_list = vendor_list.filter(
            Q(vendor_name__icontains=query) |
            # Q(material_sold__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email_address__icontains=query)
        )
        products = products.filter(
            # Q(item_name__icontains=query) |
            Q(description__icontains=query) |
            Q(variation__icontains=query)
        )
    else:
        items = Item.objects.all()
        vendor_list = Vendors.objects.all()
        products = Product.objects.all()

    # product_page = request.GET.get('product_page')
    # product_paginator = Paginator(products, items_per_page)
    # try:
    #     products = product_paginator.page(product_page)
    # except PageNotAnInteger:
    #     products = product_paginator.page(1)
    # except EmptyPage:
    #     products = product_paginator.page(product_paginator.num_pages)

    # # Handle pagination for categories
    # items_page = request.GET.get('items_page')
    # item_paginator = Paginator(items, items_per_page)
    # try:
    #     items = item_paginator.page(items_page)
    # except PageNotAnInteger:
    #     categories = item_paginator.page(1)
    # except EmptyPage:
    #     categories = item_paginator.page(item_paginator.num_pages)

    # # Handle pagination for suppliers
    # supplier_page = request.GET.get('supplier_page')
    # supplier_paginator = Paginator(vendor_list, items_per_page)
    # try:
    #     vendor_list = supplier_paginator.page(supplier_page)
    # except PageNotAnInteger:
    #     vendor_list = supplier_paginator.page(1)
    # except EmptyPage:
    #     vendor_list = supplier_paginator.page(supplier_paginator.num_pages)

    return render(request, 'admin_dashboard/tables.html', 
                  {
                      'query': query,
                      'categories':categories, 
                      'vendor_list':vendor_list, 
                      'items':items,
                      'products':products,
                      })

@admin_required    
def edit(request, pk):
    item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_item_form = EditItemForm(request.POST, request.FILES, instance=item)
        
        if edit_item_form.is_valid():
            edit_item_form.save()
            
            return redirect('admin_dashboard:tables')
    else:
        edit_item_form = EditItemForm(instance=item)
        
    return render(request, 'admin_dashboard/edit_product.html',{
        'edit_item_form': edit_item_form,
        'title':'Edit item',
    })

@admin_required    
def edit_items(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item_edit_form = ItemEditForm(request.POST, request.FILES, instance=item)
        
        if item_edit_form.is_valid():
            item_edit_form.save()
            
            return redirect('admin_dashboard:tables', pk=item.id)
    else:
        item_edit_form = ItemEditForm(instance=item)
        
    return render(request, 'admin_dashboard/edit_item.html',{
        'item_edit_form': item_edit_form,
        'title':'Edit item',
    })

@admin_required    
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_edit_form = EditCategoryForm(request.POST, request.FILES, instance=category)
        
        if category_edit_form.is_valid():
            category_edit_form.save()
            
            return redirect('admin_dashboard:tables')
    else:
        category_edit_form = EditCategoryForm(instance=category)
        
    return render(request, 'admin_dashboard/edit_category.html',{
        'category_edit_form': category_edit_form,
        'title':'Edit category',
    })

@admin_required    
def edit_vendor(request, pk):
    vendor = get_object_or_404(Vendors, pk=pk, created_by=request.user)
    if request.method == 'POST':
        vendor_edit_form = EditVendorForm(request.POST, request.FILES, instance=vendor)
        
        if vendor_edit_form.is_valid():
            vendor_edit_form.save()
            
            return redirect('admin_dashboard:tables', pk=vendor.id)
    else:
        vendor_edit_form = EditVendorForm(instance=vendor)
        
    return render(request, 'admin_dashboard/edit_vendor.html',{
        'vendor_edit_form': vendor_edit_form,
        'title':'Edit Vendor',
    })

@admin_required    
def edit_material(request, pk):
    material = get_object_or_404(Material, pk=pk, created_by=request.user)
    if request.method == 'POST':
        material_edit_form = EditMaterialForm(request.POST, request.FILES, instance=material)
        
        if material_edit_form.is_valid():
            material_edit_form.save()
            
            return redirect('admin_dashboard:tables', pk=material.id)
    else:
        material_edit_form = EditMaterialForm(instance=material)
        
    return render(request, 'admin_dashboard/edit_material.html',{
        'material_edit_form': material_edit_form,
        'title':'Edit Material',
    })

@admin_required    
def edit_paper_size(request, pk):
    paper_size = get_object_or_404(PaperSize, pk=pk, created_by=request.user)
    if request.method == 'POST':
        paper_size_edit_form = EditPaperSizeForm(request.POST, request.FILES, instance=paper_size)
        
        if paper_size_edit_form.is_valid():
            paper_size_edit_form.save()
            
            return redirect('admin_dashboard:tables', pk=paper_size.id)
    else:
        paper_size_edit_form = EditPaperSizeForm(instance=paper_size)
        
    return render(request, 'admin_dashboard/edit_paper_size.html',{
        'paper_size_edit_form': paper_size_edit_form,
        'title':'Edit Paper Sizes',
    })

@admin_required    
def edit_material_size(request, pk):
    material_size = get_object_or_404(MaterialSize, pk=pk, created_by=request.user)
    if request.method == 'POST':
        material_size_edit_form = EditPaperSizeForm(request.POST, request.FILES, instance=material_size)
        
        if material_size_edit_form.is_valid():
            material_size_edit_form.save()
            
            return redirect('admin_dashboard:tables', pk=material_size.id)
    else:
        material_size_edit_form = EditPaperSizeForm(instance=material_size)
        
    return render(request, 'admin_dashboard/edit_material_size.html',{
        'material_size_edit_form': material_size_edit_form,
        'title':'Edit Material Sizes',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Product, id=pk)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{item.variation} has been deleted successfully.')
        return redirect('admin_dashboard:product_list')  # Replace 'user_list' with your actual user list view name
    
    return render(request, 'admin_dashboard/product_delete.html', {'item': item})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, f'Category, {category.name} has been deleted successfully.')
        return redirect('admin_dashboard:product_list')  # Replace 'user_list' with your actual user list view name
    
    return render(request, 'admin_dashboard/delete_category.html', {'category': category})

@login_required
def delete_vendor(request, pk):
    vendor = get_object_or_404(Vendors, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        messages.success(request, f'Vendor, {vendor.vendor_name} has been deleted successfully.')
        return redirect('admin_dashboard:table')  # Replace 'user_list' with your actual user list view name
    
    return render(request, 'admin_dashboard/delete_vendor.html', {'vendor': vendor})

@login_required
def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, f'Material, {material.material} has been deleted successfully.')
        return redirect('admin_dashboard:table')  # Replace 'user_list' with your actual user list view name
    
    return render(request, 'admin_dashboard/delete_material.html', {'material': material})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'Item, {item.name} has been deleted successfully.')
        return redirect('admin_dashboard:table')  # Replace 'user_list' with your actual user list view name
    
    return render(request, 'admin_dashboard/delete_items.html', {'item': item})

@login_required
def delete_material_size(request, pk):
    material_size = get_object_or_404(MaterialSize, pk=pk)
    if request.method == 'POST':
        material_size.delete()
        messages.success(request, f'Material Size, {material_size.unit} has been deleted successfully.')
        return redirect('admin_dashboard:table')  # Replace 'user_list' with your actual user list view name
    
    return render(request, 'admin_dashboard/delete_material_size.html', {'material_size': material_size})

@login_required
def delete_paper_size(request, pk):
    paper_size = get_object_or_404(PaperSize, pk=pk)
    if request.method == 'POST':
        paper_size.delete()
        messages.success(request, f'Material Size, {paper_size.name} has been deleted successfully.')
        return redirect('admin_dashboard:table')  # Replace 'user_list' with your actual user list view name
    
    return render(request, 'admin_dashboard/delete_paper_size.html', {'paper_size': paper_size})

@admin_required
def product_list(request):
    query = request.GET.get('query', '').strip()
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(item_name__icontains=query) |
            Q(description__icontains=query) |
            Q(variation__icontains=query)
        )

    paginator = Paginator(products, 10)  # Show 10 products per page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'admin_dashboard/product_list.html', {'products': products, 'query': query})

@admin_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'admin_dashboard/product_details.html', {'product': product})

@admin_required
def VendorOrders(request, pk):
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST)
        if vendor_form.is_valid():
            product_id = vendor_form.cleaned_data['product_id']
            quantity = vendor_form.cleaned_data['quantity']
            # Call function to place order with vendor
            place_order(product_id, quantity)  
            return render(request, 'order_placed.html')
        else:
            vendor_form = VendorForm()
    
    return render(request, 'place_order.html', {'vendor_form': vendor_form})

def order_outsourced_products(request, is_outsourced):
    outsourced_product = get_object_or_404(Product, pk=is_outsourced)


def confirm_product_availability(request, pk):
    order = get_object_or_404(VendorOrder, pk=pk)
    order.status = 'Confirmed'
    order.save()
    return render(request, 'admin_dashboard/confirmation_received.html', {'order': order})

@admin_required
def user_list(request):
    query = request.GET.get('query', '').strip()
    users = User.objects.all()

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    paginator = Paginator(users, 10)  # Show 10 users per page
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    return render(request, 'admin_dashboard/user_list.html', {'users': users, 'query': query})

@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        edit_user_form = EditUserForm(request.POST, instance=user)
        if edit_user_form.is_valid():
            edit_user_form.save()
            messages.success(request, f'User {user.username} has been updated successfully.')
            return redirect('admin_dashboard:user_list')  # Replace 'user_list' with your actual user list view name
        else:
            messages.error(request, 'Form submission failed. Please correct the errors below.')
    else:
        edit_user_form = EditUserForm(instance=user)
    
    return render(request, 'admin_dashboard/edit_user.html', {'edit_user_form': edit_user_form, 'user': user})

@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User {user.username} has been deleted successfully.')
        return redirect('admin_dashboard:user_list')  # Replace 'user_list' with your actual user list view name
    
    return render(request, 'admin_dashboard/delete_user.html', {'user': user})