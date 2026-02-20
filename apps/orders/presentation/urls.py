from django.urls import path

from .views import (
    OrderListCreateView,
    OrderDetailView,
    OrderAssignView,
    OrderCancelView
)

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:order_id>/assign/", OrderAssignView.as_view(), name="order-assign"),
    path("orders/<int:order_id>/cancel/", OrderCancelView.as_view(), name="order-cancel"),
]
