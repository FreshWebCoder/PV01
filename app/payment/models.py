from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Transaction(models.Model):
    TYPE_DEPOSIT = 'DEPOSIT'
    TYPE_WITHDRAW = 'WITHDRAW'

    TYPE_CHOICES = (
        (TYPE_DEPOSIT, 'Deposit'), (TYPE_WITHDRAW, 'Withdraw'),
    )

    CURRENCY_USD = 'USD'
    CURRENCY_EURO = 'EURO'
    CURRENCY_CHOICES = (
        (CURRENCY_USD, '$'), (CURRENCY_USD, '€'),
    )

    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_DEPOSIT, max_length=16)
    currency = models.CharField(choices=CURRENCY_CHOICES, default=CURRENCY_USD, max_length=8)
    amount = models.FloatField()
    total_balance = models.FloatField(default=0)
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} - {self.amount}{self.currency}.'

    class Meta:
        ordering = ['-date']
