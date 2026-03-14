from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class AgentRegistrationForm(UserCreationForm):
    """Registration form for new agents"""
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email Address'
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone Number (e.g. 08012345678)'
        })
    )
    company_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Company / Agency Name'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose a Username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'company_name', 'username', 'password1', 'password2']


class AgentLoginForm(AuthenticationForm):
    """Login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password'
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating agent profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'company_name', 'company_address', 'company_logo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'company_name': forms.TextInput(attrs={'class': 'form-input'}),
            'company_address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }

from .models import AgentInvitation

class InviteAgentForm(forms.ModelForm):
    """Form for Super Admin to invite new agents"""
    class Meta:
        model = AgentInvitation
        fields = ['email', 'company_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Agent Email'}),
            'company_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Company or Agency Name (Optional)'}),
        }

class AcceptInviteForm(UserCreationForm):
    """Form for invited agents to set up their account"""
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Choose a Username'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone']
