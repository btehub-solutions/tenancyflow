from django.contrib import admin
from .models import User, AgentInvitation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'company_name', 'is_verified', 'created_at')
    list_filter = ('role', 'is_verified', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company_name')

@admin.register(AgentInvitation)
class AgentInvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'company_name', 'invited_by', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('email', 'company_name')
