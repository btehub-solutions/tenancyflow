from django.db import models
from properties.models import Property
from decimal import Decimal


class Tenant(models.Model):
    """A tenant occupying a unit in a property"""

    building = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='tenants',
        verbose_name='Property'
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    flat_or_room = models.CharField(
        max_length=100,
        help_text="e.g. Flat 3, Room 2B, Shop 5"
    )
    
    # Financial Details (matching the Excel template)
    rent_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Annual rent amount in Naira"
    )
    agreement_fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    caution_fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    
    # Tenancy Period
    tenancy_start = models.DateField(null=True, blank=True)
    tenancy_end = models.DateField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['flat_or_room', 'name']

    def __str__(self):
        return f"{self.name} - {self.flat_or_room} ({self.building.name})"

    @property
    def total_due(self):
        """Total amount due = Rent + Agreement Fee + Caution Fee"""
        return self.rent_amount + self.agreement_fee + self.caution_fee

    @property
    def total_paid(self):
        """Sum of all confirmed payments"""
        return self.payments.filter(
            status='confirmed'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

    @property
    def balance(self):
        """Outstanding balance"""
        return self.total_due - self.total_paid

    @property
    def is_fully_paid(self):
        return self.balance <= 0

    @property
    def tenancy_status(self):
        from django.utils import timezone
        today = timezone.now().date()
        if not self.is_active:
            return 'inactive'
        if self.tenancy_end and self.tenancy_end < today:
            return 'expired'
        if self.tenancy_end and (self.tenancy_end - today).days <= 30:
            return 'expiring_soon'
        return 'active'
