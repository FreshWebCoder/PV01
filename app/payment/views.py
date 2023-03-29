from django.shortcuts import render
from django import forms
from django.views.generic.edit import FormView
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Transaction
from .serializer import TransactionSerializer


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'user']


class ProcessFormView(FormView):
    template_name = 'process.html'
    form_class = ProcessForm
    success_url = '/home'

    def form_valid(self, form):
        ret = super().form_valid(form)
        user = form.cleaned_data['user']
        prev = user.transactions.first()

        from django.db.transaction import atomic

        with atomic():
            amount = prev.total_balance if prev else 0
            if form.cleaned_data['type'] == Transaction.TYPE_DEPOSIT:
                amount += form.cleaned_data['amount']
            else:
                amount -= form.cleaned_data['amount']

            transaction = form.save(commit=False)

            # To avoid the concurrency update, it will load the previous record and confirm if there's no new update.
            # This will be useful when there are many requests coming for same user in short amount of time.
            new_p = user.transactions.first()
            if new_p.pk != prev.pk:
                raise Exception('Concurrency issue happened. It will revert this action.')

            transaction.total_balance = amount
            transaction.save()
        return ret


def home(request):
    """View function for home page of site."""
    return render(request, 'index.html', context={'total': Transaction.objects.count()})


class GetBalance(APIView):
    """
    View to get balance for given user on specific date

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        date = timezone.now()
        if request.GET.get('date'):
            # /api/v1/get_balance?date=2021-04-29T21:00:00Z
            date = parse_datetime(request.GET.get('date'))
        transaction = self.request.user.transactions.filter(date__lte=date).first()

        if not transaction:
            raise NotFound

        data = TransactionSerializer(transaction).data
        return Response(data)
