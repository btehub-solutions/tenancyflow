from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
from properties.models import Property
from tenants.models import Tenant
from payments.models import Payment


@login_required
def dashboard_index(request):
    user = request.user
    
    # Get agent's data
    properties = Property.objects.filter(owner=user)
    tenants = Tenant.objects.filter(building__owner=user)
    payments = Payment.objects.filter(tenant__building__owner=user)
    
    # Summary stats
    total_properties = properties.count()
    total_tenants = tenants.filter(is_active=True).count()
    total_units = properties.aggregate(total=models.Sum('total_units'))['total'] or 0
    occupied_units = tenants.filter(is_active=True).count()
    vacant_units = max(0, total_units - occupied_units)
    
    # Financial summaries
    total_revenue = payments.filter(status='confirmed').aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    total_rent_due = tenants.filter(is_active=True).aggregate(
        total=models.Sum('rent_amount')
    )['total'] or 0
    
    total_outstanding = sum(t.balance for t in tenants.filter(is_active=True))
    
    # Recent activity
    recent_payments = payments.order_by('-created_at')[:5]
    recent_tenants = tenants.order_by('-created_at')[:5]
    
    # Expiring tenancies (next 30 days)
    today = timezone.now().date()
    thirty_days = today + timezone.timedelta(days=30)
    expiring_tenancies = tenants.filter(
        is_active=True,
        tenancy_end__gte=today,
        tenancy_end__lte=thirty_days
    ).select_related('building')
    
    # Occupancy rate
    occupancy_rate = round((occupied_units / total_units * 100), 1) if total_units > 0 else 0
    
    context = {
        'total_properties': total_properties,
        'total_tenants': total_tenants,
        'total_units': total_units,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'occupancy_rate': occupancy_rate,
        'total_revenue': total_revenue,
        'total_rent_due': total_rent_due,
        'total_outstanding': total_outstanding,
        'recent_payments': recent_payments,
        'recent_tenants': recent_tenants,
        'expiring_tenancies': expiring_tenancies,
        'properties': properties[:6],
    }
    return render(request, 'dashboard/index.html', context)
