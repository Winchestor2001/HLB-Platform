from rest_framework.serializers import ModelSerializer
from . import models


class PaymentInvoiceSerializer(ModelSerializer):
    class Meta:
        model = models.PaymentInvoice
        fields = '__all__'
