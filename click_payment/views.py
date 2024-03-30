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


class StatusInvoiceAPIView(APIView):
    def get(self, request, *args, **kwargs):
        payment_status = request.GET.get('payment_status')
        print(payment_status)
        return Response(request.GET)
