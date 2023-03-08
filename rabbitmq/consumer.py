import pika
from typing import Optional


class Consumer(object):
    def __init__(self, host: Optional[str] = 'localhost',
                 exchange: Optional[str] = 'partial_messages',
                 routing_key: Optional[str] = 'tr151199',
                 ):
        self.host = host
        self.exchange = exchange
        self.routing_key = routing_key
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
        self.channel.basic_qos(
            prefetch_count=1)  # Это гарантирует, что во время обработки будет получено только одно сообщение!
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(
            exchange=self.exchange, queue=self.queue_name, routing_key=self.routing_key)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    @staticmethod
    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
        ch.basic_ack(
            delivery_tag=method.delivery_tag)  # Это гарантирует, что если ваш потребитель сломается,
        # данные, которые он получил
        # должен быть отправлен другому потребителю!

    def consume(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback)
        self.channel.start_consuming()
