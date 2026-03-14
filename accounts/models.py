from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for TenancyFlow"""
    
    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        AGENT = 'agent', 'Agent'
        STAFF = 'staff', 'Staff'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.AGENT,
    )
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    company_address = models.TextField(blank=True)
    company_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_agent(self):
        return self.role == self.Role.AGENT

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN

    @property
    def total_properties(self):
        return self.properties.count()

    @property
    def total_tenants(self):
        from tenants.models import Tenant
        return Tenant.objects.filter(building__owner=self).count()


import uuid
from datetime import timedelta
from django.utils import timezone

class AgentInvitation(models.Model):
    """Invitation sent to prospective agents by super admin"""
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=200, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invited_by = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='sent_invitations'
    )
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invite for {self.email}"

    @property
    def is_expired(self):
        # Invitation expires in 7 days
        return self.created_at + timedelta(days=7) < timezone.now() or self.is_accepted
