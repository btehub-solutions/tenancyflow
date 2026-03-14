from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('add/', views.payment_create, name='create'),
    path('<int:pk>/', views.payment_detail, name='detail'),
    path('<int:pk>/delete/', views.payment_delete, name='delete'),
]
