from django.contrib import admin
from . import models


@admin.register(models.PaymentInvoice)
class PaymentInvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'payer', 'amount', 'created_at']
    list_display_links = ['id', 'payer']


