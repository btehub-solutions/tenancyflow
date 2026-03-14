from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Payment
from .forms import PaymentForm


@login_required
def payment_list(request):
    payments = Payment.objects.filter(
        tenant__building__owner=request.user
    ).select_related('tenant', 'tenant__building')
    
    search = request.GET.get('search', '')
    method_filter = request.GET.get('method', '')
    status_filter = request.GET.get('status', '')
    
    if search:
        payments = payments.filter(
            models.Q(tenant__name__icontains=search) |
            models.Q(reference__icontains=search) |
            models.Q(description__icontains=search)
        )
    if method_filter:
        payments = payments.filter(payment_method=method_filter)
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    total_collected = payments.filter(status='confirmed').aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    context = {
        'payments': payments,
        'search': search,
        'method_filter': method_filter,
        'status_filter': status_filter,
        'total_collected': total_collected,
        'total_payments': payments.count(),
    }
    return render(request, 'payments/payment_list.html', context)


@login_required
def payment_create(request):
    tenant_id = request.GET.get('tenant')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.recorded_by = request.user.get_full_name() or request.user.username
            payment.save()
            messages.success(request, f'Payment of ₦{payment.amount:,.2f} recorded for {payment.tenant.name}!')
            return redirect('payments:list')
    else:
        initial = {}
        if tenant_id:
            initial['tenant'] = tenant_id
        form = PaymentForm(user=request.user, initial=initial)
    
    return render(request, 'payments/payment_form.html', {'form': form, 'title': 'Record Payment'})


@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(
        Payment, pk=pk, tenant__building__owner=request.user
    )
    return render(request, 'payments/payment_detail.html', {'payment': payment})


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(
        Payment, pk=pk, tenant__building__owner=request.user
    )
    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Payment record deleted.')
        return redirect('payments:list')
    return render(request, 'payments/payment_confirm_delete.html', {'payment': payment})
