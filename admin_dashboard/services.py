from django.urls import reverse
from django.core.mail import send_mail

from items.models import Ordering, Product
from admin_dashboard.models import Vendors
import logging

logger = logging.getLogger(__name__)

def place_order(product_id, quantity):
    try:
        product = Product.objects.get(pk=product_id)
        vendor = Vendors.objects.get(material=product.material_used)
        
        order = Ordering.objects.create(product=product, quantity=quantity, vendor=vendor)
        logger.info(f"Order placed successfully for product_id: {product_id}, vendor_id: {vendor.id}")
        
        # Simulate payment confirmation
        order.payment_confirmed = True
        order.save()
        logger.info(f"Payment confirmed for order_id: {order.id}")
        
        # Notify the vendor
        notify_vendor(vendor.id, order.id, quantity)
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def notify_vendor(vendor_id, order_id, quantity):
    try:
        vendor = Vendors.objects.get(pk=vendor_id)
        # Replace "your_email@example.com" with the vendor's email address
        recipient_email = vendor.email
        subject = f"Order Notification for Order ID: {order_id}"
        message = f"Dear {vendor.name},\n\nYou have received an order for {quantity} units of product. \
                    Please confirm the availability of the product by clicking the link below:\n\n \
                    {reverse('confirm_product_availability', args=[order_id])}\n\n \
                    Thank you!\n\nBest regards,\nYour Company Name"
        send_mail(subject, message, 'your_company@example.com', [recipient_email], fail_silently=False)
        logger.info(f"Notification email sent to vendor {vendor.name} for order_id: {order_id}")
    except Exception as e:
        logger.error(f"An error occurred while notifying vendor: {e}")
