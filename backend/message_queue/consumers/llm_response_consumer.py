from .base_consumer import BaseConsumer

class LLMResponseConsumer(BaseConsumer):
    def __init__(self, connection, queue_name: str, callback_function):
        super().__init__(connection, queue_name)
        self.callback_function = callback_function

    def _on_message(self, ch, method, properties, body):
        self.callback_function(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._on_message
        )
        self.channel.start_consuming()
