from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from .serializers import PaymentInvoiceSerializer
from rest_framework.reverse import reverse
from environs import Env

env = Env()
env.read_env()


class CreateInvoiceAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = models.PaymentInvoice.objects.all()
    serializer_class = PaymentInvoiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                'success': True,
                'message': 'Invoice created successfully.',
                'invoice': self.create_invoice(serializer.data)
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @staticmethod
    def create_invoice(self, data):
        url = (f"https://my.click.uz/services/pay?service_id={env.str('CLICK_SERVICE_ID')}"
               f"&merchant_id={env.str('CLICK_MERCHANT_ID')}&amount={data.get('amount')}"
               f"&transaction_param={data.get('id')}"
               f"&return_url={reverse('status_invoice', request=self.request)}")
        return url


class StatusInvoiceAPIView(APIView):
    def get(self, request, *args, **kwargs):
        payment_status = request.GET.get('payment_status')
        print(payment_status)
        return Response(request.GET)
