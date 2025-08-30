from .base_consumer import BaseConsumer
import time
import threading

class LLMRequestConsumer(BaseConsumer):
    def __init__(self, connection, queue_name: str, llm_process_function, batch_size=5, max_wait_seconds=2):
        super().__init__(connection, queue_name)
        self.batch_size = batch_size
        self.max_wait_seconds = max_wait_seconds
        self.llm_process_function = llm_process_function
        self.buffer = []
        self.first_item_time = None
        self.running = True
        
        # Set prefetch to avoid overwhelming the consumer
        self.channel.basic_qos(prefetch_count=batch_size)

    def _maybe_flush(self):
        """Process batch if size reached or time elapsed"""
        if not self.buffer:
            return
            
        size_reached = len(self.buffer) >= self.batch_size
        time_reached = self.first_item_time and (time.time() - self.first_item_time) >= self.max_wait_seconds
        
        if size_reached or time_reached:
            # Extract job bodies for processing
            job_bodies = [item['body'] for item in self.buffer]
            methods = [item['method'] for item in self.buffer]
            
            # Process the batch
            self.llm_process_function(job_bodies=job_bodies)
            
            # Acknowledge all messages in the batch
            for method in methods:
                self.channel.basic_ack(delivery_tag=method.delivery_tag)
            
            # Clear buffer
            self.buffer = []
            self.first_item_time = None

    def _on_message(self, ch, method, properties, body):
        """Callback for each message received"""
        now = time.time()
        if not self.buffer:
            self.first_item_time = now
            
        self.buffer.append({'method': method, 'body': body})
        self._maybe_flush()

    def start_consuming(self):
        """Start consuming with proper message handling"""
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._on_message,
            auto_ack=False
        )
        
        try:
            while self.running:
                # Process any pending batches
                self._maybe_flush()
                
                # Process events with timeout to maintain heartbeats
                self.channel.connection.process_data_events(time_limit=0.1)
                
        except KeyboardInterrupt:
            self.running = False
            print("Consumer stopped by user")
        except Exception as e:
            print(f"Consumer error: {e}")
            self.running = False

    def stop_consuming(self):
        """Stop the consumer gracefully"""
        self.running = False


