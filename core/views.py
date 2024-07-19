from django.shortcuts import render, redirect
# from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .forms import *


def index(request):
    # if request.method == 'POST':
    #     message = request.POST['message']
    #     email = request.POST['email']
    #     name = request.POST['name']
        
    #     send_mail(
    #         'Contact Form - ' + name,
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         [email],
    #         fail_silently=False
    #     )
    return render(request, 'core/index.html')

def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if name and email and message:
            # Render the HTML template with form data
            html_content = render_to_string('core/email_template.html', {'name': name, 'email': email, 'message': message})

            # Create EmailMultiAlternatives object to include HTML content
            msg = EmailMultiAlternatives(
                subject='Contact Form Submission',
                body='This is a plain text message.',
                from_email=settings.EMAIL_HOST_PASSWORD,
                to=[settings.DEFAULT_FROM_EMAIL],
            )
            msg.attach_alternative(html_content, "text/html")  # Attach HTML content
            msg.send()
            return redirect('/')  # Render a success page
        else:
            return redirect('/#contacts')  # Render an error page if form is incomplete
    else:
        return redirect('/#contacts') 

def signup(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('/')
    
    else:
        form = signupForm()
    
    return render(request, 'core/signup.html', {
        'form':form
    })
    
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('core')
    
    else:
        form = LoginForm()
        
    return render(request, 'core/login.html', {
        'form':form
    })
    

def about(request):
    return render(request, 'core/pc_about.html')

def products(request):
    return render(request, 'core/products.html')

def order(request):
    return render(request, 'core/orders.html')

def gallery(request):
    return render(request, 'core/gallery.html')