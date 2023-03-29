from django.contrib import admin
from payment.models import Transaction


# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'total_balance', 'user')
    list_filter = ('type', 'user__username')
