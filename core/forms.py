from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
        
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your Username',
        'class':'form_input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your Password',
        'class':'form_input',
    }))
    
class signupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your Username',
        'class':'form_input'
    }))
    
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Your Email Address',
        'class':'form_input',
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your Password',
        'class':'form_input'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form_input'
    }))
    
# class Messages(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={
#         'placeholder': 'Your Name',
#         'class': 'form_input'
#     }))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={
#         'placeholder': 'Your Email',
#         'class': 'form_input'
#     }))
#     message = forms.CharField(widget=forms.Textarea(attrs={
#         'placeholder': 'Your Message',
#         'class': 'form_input'
#     }))