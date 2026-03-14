from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard:index') if request.user.is_authenticated else redirect('accounts:login')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('properties/', include('properties.urls')),
    path('tenants/', include('tenants.urls')),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
