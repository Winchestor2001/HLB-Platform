from django.urls import path
from . import views


urlpatterns = [
    path('status/', views.StatusInvoiceAPIView.as_view(), name='status_invoice'),
]
