from django.core.mail import send_mail
from .nats import nats

def order_created_handler(payload):
    order_id = payload["order_id"]
    send_mail(
        subject=f"Orden creada #{order_id}",
        message=f"Tu orden #{order_id} ha sido registrada correctamente.",
        from_email="no-reply@example.com",
        recipient_list=["cliente@example.com"]
    )

def order_paid_handler(payload):
    order_id = payload["order_id"]
    amount = payload["amount"]
    send_mail(
        subject=f"Pago confirmado - Orden #{order_id}",
        message=f"Se ha recibido tu pago de ${amount} para la orden #{order_id}.",
        from_email="no-reply@example.com",
        recipient_list=["cliente@example.com"]
    )

nats.subscribe("OrderCreated", order_created_handler)
nats.subscribe("OrderPaid", order_paid_handler)
