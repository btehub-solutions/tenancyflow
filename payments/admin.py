from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'amount', 'payment_date', 'payment_method', 'status', 'reference', 'created_at')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('tenant__name', 'reference', 'description')
    raw_id_fields = ('tenant',)
