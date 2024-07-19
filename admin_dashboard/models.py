from django.db import models

from django.contrib.auth.models import User

from items.models import *

# from items.models import Ordering

class Material(models.Model):
    class Meta:
        verbose_name_plural = 'materials'
        
    material = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.material

class Vendors(models.Model):
    vendor_name = models.CharField(max_length=150, unique=True)
    material_sold = models.ForeignKey(Material, related_name='material_provided', on_delete=models.CASCADE)
    price_per_unit = models.FloatField()
    phone_number = models.FloatField()
    email_address = models.EmailField(max_length=150)
    is_reliable = models.BooleanField(default=False)
    # created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.vendor_name
    
class VendorOrder(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name='material_sold', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customer_order = models.ForeignKey('items.Ordering',related_name='client_order', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order #{self.id} {self.status} Vendor Order: {self.material} (Qty: {self.quantity}) to {self.vendor.vendor_name}"

    @property
    def calculate_price(self):
        # Implement dynamic pricing logic here
        pass
