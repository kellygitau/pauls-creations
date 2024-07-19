from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


from .models import *

from items.models import *

class AdminLoginForm(AuthenticationForm):
        
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your Username',
        'class':'form-control', 
        'id':'floatingInput',
        'placeholder':'',
        'style':'color: var(--btnprimary);'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your Password',
        'class':'form-control',
        'id':'floatingPassword',
        'placeholder':'',
        'style':'color: var(--btnprimary);'

    }))
    
class AdminSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
        'id': 'floatingEmail',
        'style':'color: var(--btnprimary);'

    }))
    
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'floatingPassword',
        'style':'color: var(--btnprimary);'

    }))
    
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'id': 'floatingPassword'
    }))
    
    job_title = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Job Title',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    department = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Department',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number',
        'id': 'phoneInput',
        'style':'color: var(--btnprimary);'

    }))
    
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))

    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    terms_of_service = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'style':'color: var(--btnprimary);'

    }))

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 
            'email', 'username', 
            'password1', 'password2', 
            'job_title', 'department', 
            'phone_number', 'address', 
            'profile_picture', 'terms_of_service'
            )
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True  # Set the user as staff
        if commit:
            user.save()
        return user

class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
        'id': 'floatingEmail',
        'style':'color: var(--btnprimary);'

    }))
    
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'user`s Username',
        'id': 'floatingInput',
        'style':'color: var(--btnprimary);'

    }))
    
    is_staff = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 
            'email', 'username', 
            'is_staff',
            )
        
class VendorForm(forms.ModelForm):
    is_reliable = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))
    class Meta:
        model = Vendors
        fields = [
            'vendor_name', 'material_sold',
            'price_per_unit', 'phone_number', 
            'email_address', 'is_reliable',
            ]        
        widgets = {
            'vendor_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'placeholder':'Name of Vendor',
                'style':'color: var(--btnprimary);'

            }),
            'material_sold': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'aria-label':'What They Sell',
                'style':'color: var(--btnprimary);'

            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'placeholder':'',
                'style':'color: var(--btnprimary);'
                }),  
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'placeholder':'',
                'style':'color: var(--btnprimary);'
                }), 
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'placeholder':'',
                'style':'color: var(--btnprimary);'

            }),
        }

class EditVendorForm(forms.ModelForm):
    is_reliable = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))
    class Meta:
        model = Vendors
        fields = [
            'vendor_name', 'material_sold',
            'price_per_unit', 'phone_number', 
            'email_address', 'is_reliable',
            ]        
        widgets = {
            'vendor_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'placeholder':'Name of Vendor',
                'style':'color: var(--btnprimary);'

            }),
            'material_sold': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'aria-label':'What They Sell',
                'style':'color: var(--btnprimary);'

            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'placeholder':'',
                'style':'color: var(--btnprimary);'
                }),  
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'placeholder':'',
                'style':'color: var(--btnprimary);'
                }), 
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'placeholder':'',
                'style':'color: var(--btnprimary);'

            }),
        }

        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Enter Category Name'}),
        }

class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Enter Category Name'}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name',]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'aria-label':'Choose the Category the Item belongs to',
                'style':'color: var(--btnprimary);',
                
                }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
        'style':'color: var(--btnprimary);',
                'placeholder':'Name Of Product/ Service'}),
        }

class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name',]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'aria-label':'Choose the Category the Item belongs to',
                'style':'color: var(--btnprimary);',
                
                }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
        'style':'color: var(--btnprimary);',
                'placeholder':'Name Of Product/ Service'}),
        }
        
class NewItemForm(forms.ModelForm):
    is_outsourced = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))
    class Meta:
        model = Product
        fields = [
            'category', 'item_name', 
            'material_used', 'variation', 
            'cost_per_unit', 'description',
            'image','paper_size','is_outsourced',
            ]        
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'placeholder':'',
                'style':'color: var(--btnprimary);',
                'aria-label':'Floating label select example'}),
            'item_name': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'style':'color: var(--btnprimary);',
                'aria-label':'Choose The Item'}),
            'material_used': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'style':'color: var(--btnprimary);',
                'aria-label':'Choose the Material Best Suited for the Product'}),
            'variation': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Variation/ Type of Item'}),
            'cost_per_unit': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Cost Per Item for the Item'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control', 
                'style':'color: var(--btnprimary);',
                'id':'formFileLg'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'id':'floatingTextarea',
                'style':'color: var(--btnprimary);height: 150px;',
                'placeholder':'Image Of Item',
                }),
            'paper_size': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'aria-label':'What Size of paper does the Item Require?'}),
        }
        
class EditItemForm(forms.ModelForm):
    is_outsourced = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))
    class Meta:
        model = Product
        fields = [
            'category', 'item_name', 
            'material_used', 'variation', 
            'cost_per_unit', 'description',
            'image', 'paper_size','is_outsourced',
            ]   
          
           
        widgets = {
           'category': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'placeholder':'', 
                'style':'color: var(--btnprimary);',
                'aria-label':'Floating label select example'}),
            'item_name': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'style':'color: var(--btnprimary);',
                'aria-label':'Choose The Item'}),
            'material_used': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'style':'color: var(--btnprimary);',
                'aria-label':'Choose the Material Best Suited for the Product'}),
            'variation': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Variation/ Type of Item'}),
            'cost_per_unit': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Cost Per Item for the Item'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'style':'color: var(--btnprimary);', 
                'id':'formFileLg'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'id':'floatingTextarea',
                'placeholder':'Image Of Item',
                'style':'color: var(--btnprimary); height: 150px;',
                }),
            'paper_size': forms.Select(attrs={
                'class': 'form-select', 
                'id':'floatingSelect',
                'aria-label':'What Size of paper does the Item Require?'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('material',)        
        widgets = {
            'material': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':''
            }),
        }

class EditMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('material',)        
        widgets = {
            'material': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':''
            }),
        }

class PaperSizeForm(forms.ModelForm):
    width = forms.DecimalField(widget=forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Size of Paper'}))
    height = forms.DecimalField(widget=forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Width of Paper'}))
    class Meta:
        model = PaperSize
        fields = ('name','width','height',)        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Height of Paper'
            }),
        }

class EditPaperSizeForm(forms.ModelForm):
    width = forms.DecimalField(widget=forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Size of Paper'}))
    height = forms.DecimalField(widget=forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Width of Paper'}))
    class Meta:
        model = PaperSize
        fields = ('name','width','height',)        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Height of Paper'
            }),
        }

class MaterialSizeForm(forms.ModelForm):
    unit = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
        'style':'color: var(--btnprimary);',
        'id': 'floatingInput'
    }))
    width = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 
                'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Height of Paper'}))
    height = forms.DecimalField(widget=forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Height of Paper'}))
    class Meta:
        model = MaterialSize
        fields = ('unit','width','height',)

class EditMaterialSizeForm(forms.ModelForm):
    unit = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
        'style':'color: var(--btnprimary);',
        'id': 'floatingInput'
    }))
    width = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 
                'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Height of Paper'}))
    height = forms.DecimalField(widget=forms.NumberInput(attrs={
                'class': 'form-control', 
                'id':'floatingInput',
                'style':'color: var(--btnprimary);',
                'placeholder':'Height of Paper'}))
    class Meta:
        model = MaterialSize
        fields = ('unit','width','height',)