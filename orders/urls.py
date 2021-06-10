from django.urls import path
from .import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('transaction/<int:amount>/', views.transaction, name='transaction'),
    path('payment_success/', views.payment_success, name='payment_success')
]