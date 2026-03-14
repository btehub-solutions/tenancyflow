from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'city', 'state', 'property_type',
                  'status', 'total_units', 'landlord_name', 'landlord_phone',
                  'landlord_email', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Sunshine Villa, Block A'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Full property address'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Lagos'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Lagos'}),
            'property_type': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'total_units': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'landlord_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Landlord full name'}),
            'landlord_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '08012345678'}),
            'landlord_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'landlord@email.com'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Brief description of the property'}),
        }
