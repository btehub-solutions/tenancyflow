from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Tenant
from .forms import TenantForm


@login_required
def tenant_list(request):
    tenants = Tenant.objects.filter(building__owner=request.user).select_related('building')
    
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    property_filter = request.GET.get('property', '')
    
    if search:
        tenants = tenants.filter(
            models.Q(name__icontains=search) |
            models.Q(phone__icontains=search) |
            models.Q(flat_or_room__icontains=search)
        )
    if status_filter == 'active':
        tenants = tenants.filter(is_active=True)
    elif status_filter == 'inactive':
        tenants = tenants.filter(is_active=False)
    if property_filter:
        tenants = tenants.filter(building_id=property_filter)
    
    properties = request.user.properties.all()
    
    context = {
        'tenants': tenants,
        'properties': properties,
        'search': search,
        'status_filter': status_filter,
        'property_filter': property_filter,
        'total_tenants': tenants.count(),
    }
    return render(request, 'tenants/tenant_list.html', context)


@login_required
def tenant_create(request):
    property_id = request.GET.get('property')
    
    if request.method == 'POST':
        form = TenantForm(request.POST, user=request.user)
        if form.is_valid():
            tenant = form.save()
            messages.success(request, f'Tenant "{tenant.name}" has been added!')
            return redirect('tenants:detail', pk=tenant.pk)
    else:
        initial = {}
        if property_id:
            initial['building'] = property_id
        form = TenantForm(user=request.user, initial=initial)
    
    return render(request, 'tenants/tenant_form.html', {'form': form, 'title': 'Add New Tenant'})


@login_required
def tenant_detail(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk, building__owner=request.user)
    payments = tenant.payments.all()
    
    context = {
        'tenant': tenant,
        'payments': payments,
    }
    return render(request, 'tenants/tenant_detail.html', context)


@login_required
def tenant_update(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk, building__owner=request.user)
    
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tenant "{tenant.name}" has been updated!')
            return redirect('tenants:detail', pk=tenant.pk)
    else:
        form = TenantForm(instance=tenant, user=request.user)
    
    return render(request, 'tenants/tenant_form.html', {'form': form, 'title': 'Edit Tenant', 'tenant': tenant})


@login_required
def tenant_delete(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk, building__owner=request.user)
    
    if request.method == 'POST':
        name = tenant.name
        tenant.delete()
        messages.success(request, f'Tenant "{name}" has been removed.')
        return redirect('tenants:list')
    
    return render(request, 'tenants/tenant_confirm_delete.html', {'tenant': tenant})
