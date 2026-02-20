from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.payments.application.services import PaymentService
from apps.payments.infrastructure.repositories import DjangoPaymentRepository
from apps.orders.infrastructure.repositories import DjangoOrderRepository
from .serializers import ConfirmPaymentSerializer, RegisterPaymentSerializer



class PaymentListCreateView(APIView):

    def post(self, request):

        serializer = RegisterPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = PaymentService(
            payment_repo=DjangoPaymentRepository(),
            order_repo=DjangoOrderRepository()
        )

        payment = service.register_payment(
            order_id=serializer.validated_data["order_id"],
            amount=serializer.validated_data["amount"]
        )

        return Response({
            "id": payment.id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "status": payment.status.value
        }, status=status.HTTP_201_CREATED)



class ConfirmPaymentView(APIView):

    def post(self, request, payment_id):

        service = PaymentService(
            payment_repo=DjangoPaymentRepository(),
            order_repo=DjangoOrderRepository()
        )

        payment = service.confirm_payment(payment_id)

        return Response({
            "id": payment.id,
            "order_id": payment.order_id,
            "status": payment.status.value
        })
