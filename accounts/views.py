from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import AgentInvitation
from .forms import AgentLoginForm, ProfileUpdateForm, InviteAgentForm, AcceptInviteForm


def is_super_admin(user):
    return user.is_authenticated and user.is_superuser


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    # Registration is now invite only
    messages.info(request, "TenancyFlow is an invite-only platform. Please contact us to get an invitation.")
    return redirect('accounts:login')


@user_passes_test(is_super_admin)
def invite_agent_view(request):
    if request.method == 'POST':
        form = InviteAgentForm(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            invite.invited_by = request.user
            invite.save()
            
            # Generate invite link and send email
            invite_link = request.build_absolute_uri(
                reverse('accounts:accept_invite', kwargs={'token': invite.token})
            )
            
            subject = "You've been invited to TenancyFlow!"
            message = (
                f"Hello,\n\n"
                f"You have been invited to use TenancyFlow by {request.user.get_full_name() or request.user.username}.\n\n"
                f"Click the highly secure link below to set up your property management account:\n\n"
                f"{invite_link}\n\n"
                f"Welcome on board!\n\n"
                f"- The TenancyFlow Team"
            )
            
            send_mail(
                subject,
                message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@tenancyflow.com'),
                [invite.email],
                fail_silently=False,
            )
            
            messages.success(request, f'Invitation sent securely to {invite.email}!')
            return redirect('accounts:invite_agent')
    else:
        form = InviteAgentForm()
        
    invitations = AgentInvitation.objects.all()
    return render(request, 'accounts/invite_agent.html', {
        'form': form, 
        'invitations': invitations
    })


def accept_invite_view(request, token):
    if request.user.is_authenticated:
        logout(request)
        
    invite = get_object_or_404(AgentInvitation, token=token)
    
    if invite.is_expired:
        messages.error(request, "This invitation link has expired or has already been used.")
        return redirect('accounts:login')
        
    if request.method == 'POST':
        form = AcceptInviteForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = invite.email
            user.company_name = invite.company_name
            user.role = 'agent'
            user.save()
            
            invite.is_accepted = True
            invite.save()
            
            login(request, user)
            messages.success(request, f'Welcome to TenancyFlow, {user.first_name}! Your account is securely set up.')
            return redirect('dashboard:index')
    else:
        form = AcceptInviteForm()
        
    return render(request, 'accounts/accept_invite.html', {
        'form': form, 
        'invite': invite
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = AgentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'dashboard:index')
            return redirect(next_url)
    else:
        form = AgentLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})
