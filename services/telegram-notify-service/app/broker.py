from kombu import Connection, Exchange, Queue, Consumer
from socket import timeout as timeout_err
from logging import getLogger

logger = getLogger("telegram-notify-service")

class Broker():
    def __init__(self, ampq_dsn, exchange_name = "telegram_notify", queue_name="simple_queue", exchange_type='direct'):
        self.dsn = ampq_dsn
        self.callbacks = []
        self.exchange = Exchange(exchange_name, type=exchange_type)
        self.queue = Queue(queue_name, exchange=self.exchange, routing_key=queue_name)

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def send_message(self, message):
        with Connection(self.dsn) as connection:
            producer = connection.Producer()
            producer.publish(message, exchange=self.exchange, routing_key=self.queue.routing_key)

    def run_consumer(self):
        with Connection(self.dsn) as connection:
            with connection.Consumer(self.queue, callbacks=self.callbacks) as consumer:
                logger.info("Started pooling messages")
                while True:
                    try:
                        connection.drain_events(timeout=10)
                    except timeout_err:
                        connection.heartbeat_check()
        
