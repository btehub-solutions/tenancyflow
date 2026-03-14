from django.contrib import admin
from .models import Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'flat_or_room', 'phone', 'rent_amount', 'is_active', 'tenancy_start', 'tenancy_end')
    list_filter = ('is_active', 'building', 'tenancy_start')
    search_fields = ('name', 'phone', 'email', 'flat_or_room')
    raw_id_fields = ('building',)
