from django.db import models
from tenants.models import Tenant


class Payment(models.Model):
    """Payment record for a tenant"""

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        TRANSFER = 'transfer', 'Bank Transfer'
        CHEQUE = 'cheque', 'Cheque'
        POS = 'pos', 'POS'
        ONLINE = 'online', 'Online Payment'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.TRANSFER
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED
    )
    reference = models.CharField(max_length=100, blank=True, help_text="Receipt/Reference number")
    description = models.TextField(blank=True)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    
    recorded_by = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date', '-created_at']

    def __str__(self):
        return f"₦{self.amount:,.2f} - {self.tenant.name} ({self.payment_date})"
