from ..models import *
from django.db import models


class Month(BaseModel):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

class PaymentType(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title



class Payment(BaseModel):
    student = models.ForeignKey('user_auth.Student', on_delete=models.CASCADE, related_name='payment')
    group = models.ForeignKey('user_auth.Group', on_delete=models.SET_NULL, related_name='payment', null=True, blank=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='payment', null=True, blank=True)
    payment_type = models.ForeignKey('user_auth.PaymentType', on_delete=models.CASCADE, related_name='payment')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.student.user.phone_number} - {self.price} UZS ({self.payment_type.title})"
