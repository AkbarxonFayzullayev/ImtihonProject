from django.db import models

class Payments(models.Model):
    user = models.ForeignKey('user_auth.User', on_delete=models.RESTRICT, related_name='payments')
    group = models.ForeignKey('user_auth.Group', on_delete=models.RESTRICT, null=True, blank=True)
    amount = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online')
    ])
    is_paid = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount} so'm"
