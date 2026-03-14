from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['tenant', 'amount', 'payment_date', 'payment_method',
                  'status', 'reference', 'description', 'receipt_image']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'reference': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Receipt/Reference number'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Payment description'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            from tenants.models import Tenant
            self.fields['tenant'].queryset = Tenant.objects.filter(
                building__owner=user, is_active=True
            ).select_related('building')
