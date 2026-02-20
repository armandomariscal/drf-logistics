class NATS:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name: str, callback):
        self.subscribers.setdefault(event_name, []).append(callback)

    def publish(self, event_name: str, payload):
        for cb in self.subscribers.get(event_name, []):
            cb(payload)

nats = NATS()
