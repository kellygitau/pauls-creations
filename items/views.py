import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from mpesa_api.core import MpesaClient
import stripe
import paypalrestsdk

from admin_dashboard.models import VendorOrder
from .models import *
from .forms import PaymentForm, ClientOrderingForm
from .utils import upload_to_google_drive
from admin_dashboard.services import place_order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import logging

logger = logging.getLogger(__name__)

def items(request):
    query = request.GET.get('query', '').strip()
    items = Product.objects.all()

    if query:
        items = items.filter(
            Q(item_name__icontains=query) |
            Q(description__icontains=query) |
            Q(variation__icontains=query)
        )

    return render(request, 'items/index.html', {
        'items': items, 
        'query': query,
        })


def upload_to_google_drive(file_path, file_name):
    """Uploads a file to Google Drive."""
    creds = Credentials.service_account_credentials(
        os.path.join(settings.BASE_DIR, 'client_secrets.json'),
        scopes=['https://www.googleapis.com/auth/drive']
    )

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def Client_order(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        ordering_form = ClientOrderingForm(request.POST, request.FILES)
        
        if payment_form.is_valid() and ordering_form.is_valid():
            try:
                # Save payment details to the database
                payment_instance = payment_form.save()

                # Save ordering details to the database
                ordering_instance = ordering_form.save(commit=False)
                ordering_instance.is_paid = payment_instance
                ordering_instance.save()

                # Create a VendorOrder entry for the material used
                material_used = ordering_instance.product.material_used
                VendorOrder.objects.create(material=material_used)

                # Upload client images and files to Google Drive
                for client_image in request.FILES.getlist('client_images'):
                    upload_to_google_drive(client_image, client_image.name)
                for client_file in request.FILES.getlist('client_files'):
                    upload_to_google_drive(client_file, client_file.name)

                messages.success(request, 'Payment and files uploaded successfully!')
                return redirect('success_page')  # Replace 'success_page' with your success URL
                
            except Exception as e:
                logger.error(f"Error during order processing: {e}")
                messages.error(request, 'There was an error processing your request. Please try again.')
                
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        payment_form = PaymentForm()
        ordering_form = ClientOrderingForm()
        
    return render(request, 'combined_form.html', {'payment_form': payment_form, 'ordering_form': ordering_form})

# def checkout(request, pk):
#     item = Product.objects.get(id=pk)
#     if request.method == 'POST':

        

# def customer_order(request):
#     if request.method == 'POST':
#         customer_order_form = ClientOrderingForm(request.POST)
#         if customer_order_form.is_valid():
#             product_id = customer_order_form.cleaned_data['product_id']
#             quantity = customer_order_form.cleaned_data['quantity']
#             place_order(product_id, quantity)
#             return render(request, 'order_placed.html')
#     else:
#         form = ClientOrderingForm()
    
#     return render(request, 'place_order.html', {'form': form})

# mpesa_client = MpesaClient(
#     consumer_key=settings.MPESA_CONSUMER_KEY,
#     consumer_secret=settings.MPESA_CONSUMER_SECRET,
#     shortcode=settings.MPESA_SHORTCODE,
#     passkey=settings.MPESA_PASSKEY
# )

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

# mpesa_client = MpesaClient(
#     consumer_key=settings.MPESA_CONSUMER_KEY,
#     consumer_secret=settings.MPESA_CONSUMER_SECRET,
#     shortcode=settings.MPESA_SHORTCODE,
#     passkey=settings.MPESA_PASSKEY
# )

def checkout_view(request):
    if request.method == 'POST':
        checkout_form = ClientOrderingForm(request.POST)
        if checkout_form.is_valid():
            amount = checkout_form.cleaned_data['amount']
            payment_method = checkout_form.cleaned_data['payment_method']

            transaction = Payment.objects.create(
                amount=amount,
                payment_method=payment_method,
                status='pending'
            )

            if payment_method == 'stripe':
                # Stripe payment logic
                intent = stripe.PaymentIntent.create(
                    amount=int(amount * 100),
                    currency='usd',
                    metadata={'transaction_id': transaction.id}
                )
                transaction.transaction_id = intent.id
                transaction.save()
                return render(request, 'payment/stripe.html', {'client_secret': intent.client_secret})

            elif payment_method == 'paypal':
                # PayPal payment logic
                payment = paypalrestsdk.Payment({
                    "intent": "sale",
                    "payer": {"payment_method": "paypal"},
                    "transactions": [{"amount": {"total": str(amount), "currency": "USD"}}],
                    "redirect_urls": {
                        "return_url": request.build_absolute_uri('/paypal/return/'),
                        "cancel_url": request.build_absolute_uri('/paypal/cancel/')
                    }
                })
                if payment.create():
                    transaction.transaction_id = payment.id
                    transaction.save()
                    for link in payment.links:
                        if link.method == "REDIRECT":
                            redirect_url = link.href
                            return redirect(redirect_url)
                else:
                    transaction.status = 'failed'
                    transaction.save()
                    return render(request, 'payment/failed.html')

            # elif payment_method == 'mpesa':
            #     # M-Pesa payment logic
            #     response = mpesa_client.stk_push(
            #         phone_number='254700000000',
            #         amount=int(amount),
            #         account_reference='ref',
            #         transaction_desc='desc'
            #     )
            #     if response['ResponseCode'] == '0':
            #         transaction.transaction_id = response['CheckoutRequestID']
            #         transaction.save()
            #         return render(request, 'payment/mpesa.html', {'transaction': transaction})
            #     else:
            #         transaction.status = 'failed'
            #         transaction.save()
            #         return render(request, 'payment/failed.html')

    else:
        checkout_form = ClientOrderingForm()

    return render(request, 'items/checkout.html', {'checkout_form': checkout_form})

def paypal_return(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        transaction = Payment.objects.get(transaction_id=payment_id)
        transaction.status = 'completed'
        transaction.save()
        return render(request, 'payment/success.html', {'transaction': transaction})
    else:
        transaction = Payment.objects.get(transaction_id=payment_id)
        transaction.status = 'failed'
        transaction.save()
        return render(request, 'payment/failed.html')

def paypal_cancel(request):
    return render(request, 'payment/cancel.html')
