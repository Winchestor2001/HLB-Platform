from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.CreateInvoiceAPIView.as_view(), name='create_invoice'),
    path('status/', views.StatusInvoiceAPIView.as_view(), name='status_invoice'),
]
