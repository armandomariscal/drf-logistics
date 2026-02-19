from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.orders.infrastructure.repositories import DjangoOrderRepository
from apps.orders.application.services import OrderService

from .serializers import (
    CreateOrderSerializer,
    OrderSerializer
)


def get_order_service():

    repository = DjangoOrderRepository()

    service = OrderService(repository)

    return service


class OrderListCreateView(APIView):

    def post(self, request):

        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = get_order_service()

        order = service.create_order(
            tracking_number=serializer.validated_data["tracking_number"],
            customer_name=serializer.validated_data["customer_name"],
            origin=serializer.validated_data["origin"],
            destination=serializer.validated_data["destination"],
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )


    def get(self, request):

        service = get_order_service()

        orders = service.list_orders()

        return Response(
            OrderSerializer(orders, many=True).data
        )


class OrderDetailView(APIView):

    def get(self, request, order_id):

        service = get_order_service()

        order = service.get_order(order_id)

        return Response(
            OrderSerializer(order).data
        )


class OrderAssignView(APIView):

    def post(self, request, order_id):

        repository = DjangoOrderRepository()
        service = OrderService(repository)

        driver_id = request.data.get("driver_id")

        order = service.assign_order(
            order_id=order_id,
            driver_id=driver_id
        )

        return Response({
            "id": order.id,
            "status": order.status,
            "driver_id": order.driver_id
        })


class OrderCancelView(APIView):

    def post(self, request, order_id):

        repository = DjangoOrderRepository()
        service = OrderService(repository)

        order = service.cancel_order(order_id)

        return Response({
            "id": order.id,
            "status": order.status
        })
