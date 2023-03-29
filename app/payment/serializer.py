from rest_framework import serializers

from .models import Transaction


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('type', 'date', 'amount', 'total_balance')


class TransactionSerializer(serializers.ModelSerializer):
    histories = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('total_balance', 'date', 'histories')

    def get_histories(self, instance):
        return TransactionListSerializer(instance.user.transactions.filter(date__lte=instance.date), many=True).data
