from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'property_type', 'status', 'total_units', 'occupied_units', 'created_at')
    list_filter = ('property_type', 'status', 'state', 'city')
    search_fields = ('name', 'address', 'landlord_name', 'owner__username')
    raw_id_fields = ('owner',)
