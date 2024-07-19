from django.db import models
from django.contrib.auth.models import User

import random
import string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from background_task import background

from admin_dashboard.models import Material, Vendors

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return  self.name
    
class PaperSize(models.Model):
    name = models.CharField(max_length=100)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def area(self):
        return self.width * self.height

    def __str__(self):
        return f"{self.name} ({self.width} x {self.height})"
    
class MaterialSize(models.Model):
    unit = models.CharField(max_length=100)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def area(self):
        return self.width * self.height

    def __str__(self):
        return f"{self.unit} ({self.width} x {self.height})"

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    item_name = models.ForeignKey(Item, related_name='product', on_delete=models.CASCADE)
    material_used = models.ForeignKey('admin_dashboard.Material', related_name='products', on_delete=models.CASCADE)
    variation = models.CharField(max_length=150, unique=True)
    cost_per_unit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    paper_size = models.ForeignKey(PaperSize, related_name='product_size', on_delete=models.SET_NULL, null=True)
    material_size = models.ForeignKey(MaterialSize, related_name='product_size', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, related_name='created_products', on_delete=models.SET_NULL, null=True)
    is_outsourced = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} - {self.variation}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        # Add more choices as needed
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('mpesa', 'M-Pesa'),
        ('Cash on Delivery', 'Cash on Delivery'),
        # Add more choices as needed
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.method} - {self.amount} - {self.status}"

class Ordering(models.Model):
    class Meta:
        verbose_name_plural = 'Orderings'

    # Fields related to the product being ordered
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE, null=True)
    unit_ordered = models.FloatField(null=True)

    # Shipping Information
    shipping_address = models.TextField(blank=True)
    shipping_method = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=50, blank=True)

    # Payment Information
    payment = models.ForeignKey(Payment, related_name='orders', on_delete=models.CASCADE, null=True)

    # Order Status
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    
    
    customer_email = models.EmailField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    customer_notes = models.TextField(blank=True)

    product_pages =  models.FloatField(null=True)
    client_images = models.ImageField(upload_to='order_images', blank=True, null=True)
    client_files = models.FileField(upload_to='order_files', blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Constants for vat, profit, and labour_cost
    VAT_PERCENTAGE = 0.16  # Example VAT percentage
    PROFIT_PERCENTAGE = 0.10  # Example profit percentage
    LABOUR_COST = 50.00  # Example labour cost

    # Calculate total cost method
    def calculate_total_cost(self):
        total_cost = self.unit_ordered * self.product.cost_per_unit
        total_cost += total_cost * self.VAT_PERCENTAGE  # Include VAT
        total_cost += total_cost * self.PROFIT_PERCENTAGE  # Include profit
        total_cost += self.LABOUR_COST  # Include labour cost
        return total_cost

    def __str__(self):
        return f"Order of {self.product.variation} (Qty: {self.unit_ordered})"
    
    
    
# class VendorOrder(models.Model):
#     vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
#     material = models.ForeignKey(MaterialOrService, related_name='material_sold', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     customer_order = models.ForeignKey(Ordering,related_name='client_order', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Vendor Order: {self.material} (Qty: {self.quantity}) to {self.vendor.vendor_name}"