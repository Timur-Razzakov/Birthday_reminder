import pika
from typing import Optional
from logging import Logger
import logging


class Producer(object):
    def __init__(self, host: Optional[str] = 'localhost',
                 exchange: Optional[str] = 'partial_messages',
                 logger: Optional[Logger] = logging.getLogger('Producer')):
        self.host = host
        self.exchange = exchange  # обменник, от него пойдёт к очереди
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

    def produce(self, routing_key, message):
        self.channel.basic_publish(
            exchange='partial_messages',
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Постоянное сообщение! Предотвращает потерю сообщения!
            ))
        print(" [x] Sent 'message'")
        self.connection.close()
