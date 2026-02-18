from rest_framework import serializers


class CreateOrderSerializer(serializers.Serializer):

    tracking_number = serializers.CharField(max_length=100)
    customer_name = serializers.CharField(max_length=255)
    origin = serializers.CharField(max_length=255)
    destination = serializers.CharField(max_length=255)


class OrderSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    tracking_number = serializers.CharField()
    customer_name = serializers.CharField()
    origin = serializers.CharField()
    destination = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
