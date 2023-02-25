import pika
from typing import Optional


class Consumer(object):
    def __init__(self, host: Optional[str] = 'localhost',
                 exchange: Optional[str] = 'partial_messages',
                 routing_key: Optional[str] = 'mk151199',
                 ):
        self.host = host
        self.exchange = exchange
        self.routing_key = routing_key
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
        self.channel.basic_qos(prefetch_count=1)  # This ensures that only one message is received while in process !
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(
            exchange=self.exchange, queue=self.queue_name, routing_key=self.routing_key)

    @staticmethod
    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
        ch.basic_ack(delivery_tag=method.delivery_tag)  # This ensures that if your consumer crushes, the data it got
        # should be sent to another consumer !

    def consume(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback)
        self.channel.start_consuming()

    @property
    def host(self):
        return self.host

    @property
    def exchange(self):
        return self.exchange

    @property
    def routing_key(self):
        return self.routing_key

    @exchange.setter
    def exchange(self, value):
        self._exchange = value

    @host.setter
    def host(self, value):
        self._host = value

    @routing_key.setter
    def routing_key(self, value):
        self._routing_key = value