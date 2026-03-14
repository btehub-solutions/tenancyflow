from django.db import models
from django.conf import settings


class Property(models.Model):
    """A property/house managed by an agent"""
    
    class PropertyType(models.TextChoices):
        RESIDENTIAL = 'residential', 'Residential'
        COMMERCIAL = 'commercial', 'Commercial'
        MIXED = 'mixed', 'Mixed Use'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        UNDER_MAINTENANCE = 'maintenance', 'Under Maintenance'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    name = models.CharField(max_length=200, help_text="e.g. Sunshine Villa, Block A")
    address = models.TextField()
    city = models.CharField(max_length=100, default='Lagos')
    state = models.CharField(max_length=100, default='Lagos')
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.RESIDENTIAL
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    total_units = models.PositiveIntegerField(default=1, help_text="Number of flats/rooms")
    landlord_name = models.CharField(max_length=200, blank=True)
    landlord_phone = models.CharField(max_length=20, blank=True)
    landlord_email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.address[:50]}"

    @property
    def occupied_units(self):
        return self.tenants.filter(is_active=True).count()

    @property
    def vacant_units(self):
        return max(0, self.total_units - self.occupied_units)

    @property
    def occupancy_rate(self):
        if self.total_units == 0:
            return 0
        return round((self.occupied_units / self.total_units) * 100, 1)

    @property
    def total_monthly_revenue(self):
        return self.tenants.filter(is_active=True).aggregate(
            total=models.Sum('rent_amount')
        )['total'] or 0

    @property
    def total_outstanding(self):
        from payments.models import Payment
        total_due = sum(t.total_due for t in self.tenants.filter(is_active=True))
        total_paid = Payment.objects.filter(
            tenant__building=self,
            tenant__is_active=True
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        return max(0, total_due - total_paid)
