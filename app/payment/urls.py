from django.urls import path
from .views import home, ProcessFormView, GetBalance

urlpatterns = [
    path('', home, name='home'),
    path('process', ProcessFormView.as_view(), name='process'),
    path('api/v1/get_balance', GetBalance.as_view(), name='get_balance'),
]
