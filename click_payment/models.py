import uuid

from django.db import models
from student_platform.models import Student


class PaymentInvoice(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    payer = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.payer}"
