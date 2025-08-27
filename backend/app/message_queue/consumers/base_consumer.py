import pika

class BaseConsumer:
    def __init__(self, connection, queue_name: str):
        if connection is None:
            raise ValueError("A valid Pika connection is required.")

        self.connection = connection
        self.queue_name = queue_name
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def start_consuming(self):
        raise NotImplementedError("Subclasses must implement this method.")
