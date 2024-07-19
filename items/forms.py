from django import forms

from items.models import * 

from .models import Payment, Ordering

from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _

# class MultipleFileInput(ClearableFileInput):
#     template_name = 'items/custom_clearable_file_input.html' 
    
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = (
            'method', 'transaction_id', 
            'status',
            )
        widgets = {
            'method': forms.Select(attrs={'class': 'form_input'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form_input'}),
            'status': forms.Select(attrs={'class': 'form_input'}),
        }

class ClientOrderingForm(forms.ModelForm):
    
    class Meta:
        model = Ordering
        fields = [
            'product',
            'unit_ordered',
            'shipping_address',
            'shipping_method',
            'tracking_number',
            'payment',
            'status',
            'customer_email',
            'customer_phone',
            'customer_notes',
            'product_pages',
            'client_images',
            'client_files',
            'is_paid'
        ]

        widgets = {
            'product': forms.Select(attrs={'class': 'form_input'}),
            'unit_ordered': forms.NumberInput(attrs={'class': 'form_input', 'min': 0, 'step': 0.01}),
            'shipping_method': forms.TextInput(attrs={'class': 'form_input'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form_input'}),
            'payment': forms.Select(attrs={'class': 'form_input'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form_input'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form_input'}),
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'customer_notes': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(choices=Ordering.payment),
            'method': forms.Select(choices=Ordering.ORDER_STATUS_CHOICES),
            'client_images': forms.ClearableFileInput(attrs={'multiple': False}),
            'client_files': forms.ClearableFileInput(attrs={'multiple': False}),
    }