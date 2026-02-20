from rest_framework import serializers


class ConfirmPaymentSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()

class RegisterPaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
