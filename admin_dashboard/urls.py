from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    # path('signup/', views.signup, name='signup'),
    # path('login/', views.login, name='login'),
    path('data/', views.tables, name='tables'),
    path('admin_forms/', views.admin_forms, name='admin_forms'),
    path('admin_forms/add_category/', views.add_category, name='add_category'),
    path('admin_forms/add_item/', views.add_item, name='add_item'),
    path('admin_forms/add_product/', views.add_product, name='add_product'),
    path('admin_forms/add_material/', views.add_material, name='add_material'),
    path('admin_forms/add_material_size/', views.add_material_size, name='add_material_size'),
    path('admin_forms/add_paper_size/', views.add_paper_size, name='add_paper_size'),
    path('admin_forms/add_vendor/', views.add_vendor, name='add_vendor'),
    path('user_list/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.edit, name='product_edit'),
    path('items/<int:pk>/edit/', views.edit_items, name='edit_items'),
    path('category/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('vendor/<int:pk>/edit/', views.edit_vendor, name='edit_vendor'),
    path('material/<int:pk>/edit/', views.edit_material, name='edit_material'),
    path('paper_size/<int:pk>/edit/', views.edit_paper_size, name='edit_paper_size'),
    path('material_size/<int:pk>/edit/', views.edit_material_size, name='edit_material_size'), 
    path('products/<int:pk>/delete/', views.delete, name='product_delete'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('vendor/<int:pk>/delete/', views.delete_vendor, name='vendor_delete'),
    path('material/<int:pk>/delete/', views.delete_material, name='material_delete'),
    path('paper_size/<int:pk>/delete/', views.delete_paper_size, name='delete_paper_size'),
    path('material_size/<int:pk>/delete/', views.delete_material_size, name='delete_material_size'),
    path('item/<int:pk>/delete/', views.delete_item, name='item_delete'),
    path('confirm-product-availability/<int:order_id>/', views.confirm_product_availability, name='confirm_product_availability'),
]