import pika
from typing import Optional
from logging import Logger
import logging


class Producer(object):
    def __init__(self, host: Optional[str] = 'localhost',
                 exchange: Optional[str] = 'partial_messages',
                 logger: Optional[Logger] = logging.getLogger('Producer')):
        self.host = host
        self.exchange = exchange
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

    def produce(self, routing_key: Optional[str] = 'tr151199', message: Optional[str] = None):
        self.channel.basic_publish(
            exchange='partial_messages',
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent message ! Avoids the loss of message !
            ))

        self.connection.close()

    @property
    def host(self):
        return self.host

    @property
    def exchange(self):
        return self.exchange

    @host.setter
    def host(self, value):
        self._host = value

    @exchange.setter
    def exchange(self, value):
        self._exchange = value
