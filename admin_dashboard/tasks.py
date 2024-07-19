# from celery import shared_task
# from django.utils import timezone
# from .models import VendorOrder
# from admin_dashboard.services import notify_vendor

# @shared_task(schedule=60)
# def check_order_status():
#     orders = VendorOrder.objects.filter(status='Pending')
#     for order in orders:
#         if order.delivery_date and order.delivery_date < timezone.now():
#             Send a reminder email to the vendor
#             notify_vendor(order.vendor_id, order.id, order.quantity)
