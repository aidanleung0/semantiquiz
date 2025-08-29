import pika
import json
import logging


class MessageProducer:
    def __init__(self, connection):
        """
        Initialied the producer with an existing connection.
        Passing in a connection object is better because of dependency injection
        """
        self.connection = connection
        self.channel = self.connection.channel()

    def publish(self, queue_name: str, payload: dict):
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)

            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(payload),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )

            logging.info(f"Published message to queue {queue_name}")
            print(f"Published message to queue {queue_name}")
        except Exception as e:
            logging.error(f"Failed to publish meessage: {e}")
            raise
