import os
import pika
import json
import logging

def _rabbit_params():
    url = os.getenv("RABBITMQ_URL")
    if url:
        params = pika.URLParameters(url)
        return params
    return pika.ConnectionParameters(
        'rabbitmq',
        credentials=pika.PlainCredentials(os.getenv("RABBITMQ_USER", "guest"), os.getenv("RABBITMQ_PASS", "guest"))
    )

class MessageProducer:
    def __init__(self, parameters: pika.URLParameters | pika.ConnectionParameters | None = None):
        """
        Initialize the producer with an existing connection.
        Passing in a connection object is better because of dependency injection
        """
        # self.connection = connection
        # self.channel = self.connection.channel()
        self.parameters = parameters or _rabbit_params()

    def publish(self, queue_name: str, payload: dict):
        # try:
        #     self.channel.queue_declare(queue=queue_name, durable=True)

        #     self.channel.basic_publish(
        #         exchange='',
        #         routing_key=queue_name,
        #         body=json.dumps(payload),
        #         properties=pika.BasicProperties(
        #             delivery_mode=2,
        #         )
        #     )

        #     logging.info(f"Published message to queue {queue_name}")
        #     print(f"Published message to queue {queue_name}")
        # except Exception as e:
        #     logging.error(f"Failed to publish meessage: {e}")
        #     raise
        try:
            connection = pika.BlockingConnection(self.parameters)
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_publish(
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
        finally:
            try:
                connection.close()
            except Exception as e:
                pass
