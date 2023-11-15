from kombu import Connection, Exchange, Queue, Consumer
from logging import getLogger

logger = getLogger("review-service")

class MessageBroker():
    def __init__(self, ampq_dsn, exchange_name = "telegram_notify", queue_name="simple_queue", exchange_type='direct'):
        self.dsn = ampq_dsn
        self.exchange = Exchange(exchange_name, type=exchange_type)
        self.queue = Queue(queue_name, exchange=self.exchange, routing_key=queue_name)

    def send_message(self, message):
        with Connection(self.dsn) as connection:
            producer = connection.Producer()
            producer.publish(message, exchange=self.exchange, routing_key=self.queue.routing_key)
        