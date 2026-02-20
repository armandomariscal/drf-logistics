from django.urls import path
from .views import ConfirmPaymentView, PaymentListCreateView

urlpatterns = [
    path("payments/", PaymentListCreateView.as_view(), name="payment-list-create"),
    path("payments/<int:payment_id>/confirm/", ConfirmPaymentView.as_view(), name="confirm-payment"),
]
