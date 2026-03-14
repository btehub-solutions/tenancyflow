from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Property
from .forms import PropertyForm


@login_required
def property_list(request):
    properties = Property.objects.filter(owner=request.user)
    
    # Search & Filter
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    
    if search:
        properties = properties.filter(
            models.Q(name__icontains=search) |
            models.Q(address__icontains=search) |
            models.Q(landlord_name__icontains=search)
        )
    if status_filter:
        properties = properties.filter(status=status_filter)
    if type_filter:
        properties = properties.filter(property_type=type_filter)
    
    context = {
        'properties': properties,
        'search': search,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'total_properties': properties.count(),
    }
    return render(request, 'properties/property_list.html', context)


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.save()
            messages.success(request, f'Property "{prop.name}" has been added!')
            return redirect('properties:detail', pk=prop.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'properties/property_form.html', {'form': form, 'title': 'Add New Property'})


@login_required
def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    tenants = prop.tenants.all()
    
    context = {
        'property': prop,
        'tenants': tenants,
        'active_tenants': tenants.filter(is_active=True).count(),
    }
    return render(request, 'properties/property_detail.html', context)


@login_required
def property_update(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            messages.success(request, f'Property "{prop.name}" has been updated!')
            return redirect('properties:detail', pk=prop.pk)
    else:
        form = PropertyForm(instance=prop)
    
    return render(request, 'properties/property_form.html', {'form': form, 'title': 'Edit Property', 'property': prop})


@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        name = prop.name
        prop.delete()
        messages.success(request, f'Property "{name}" has been deleted.')
        return redirect('properties:list')
    
    return render(request, 'properties/property_confirm_delete.html', {'property': prop})
