from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)
    passport_data = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_name


class Admin(models.Model):
    STATUS = (
        ("Катта админ", "Катта админ"),
        ("Модератор", "Модератор"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.full_name
