from django import forms
from .models import Tenant


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['building', 'name', 'phone', 'email', 'flat_or_room',
                  'rent_amount', 'agreement_fee', 'caution_fee',
                  'tenancy_start', 'tenancy_end', 'is_active', 'remarks',
                  'emergency_contact_name', 'emergency_contact_phone']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '08012345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'tenant@email.com'}),
            'flat_or_room': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Flat 3, Room 2B'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'agreement_fee': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'caution_fee': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'tenancy_start': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'tenancy_end': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Additional notes'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Emergency contact name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '08012345678'}),
        }
        labels = {
            'building': 'Property',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['building'].queryset = user.properties.all()
