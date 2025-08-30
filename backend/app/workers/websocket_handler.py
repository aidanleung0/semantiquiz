import pika
import json
import threading
import asyncio
import os
from message_queue.consumers.llm_response_consumer import LLMResponseConsumer
from connection_manager import connection_manager
import time

def forward_result_to_websocket(body):
    """
    Callback function for the message queue consumer
    """
    try:
        data = json.loads(body)
        job_id = data.get("job_id")
        print(f"Websocket handler received message for job {job_id}: {data}", flush=True)
        
        if job_id:
            print(f"Forwarding to websocket for job {job_id}", flush=True)
            asyncio.run_coroutine_threadsafe(
                connection_manager.send_message(job_id, data),
                main_event_loop
            )
            print(f"Message forwarded successfully", flush=True)
        else:
            print("Warning: Received a message without a job_id.", flush=True)
    except Exception as e:
        print(f"An error occurred in the handler callback: {e}", flush=True)
        import traceback
        traceback.print_exc()

def run_consumer(loop):
    global main_event_loop
    main_event_loop = loop
    print(f"Setting up consumer thread with event loop: {loop}", flush=True)
    
    try:
        credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER", "guest"), os.getenv("RABBITMQ_PASS", "guest"))
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
        print("Consumer thread connected to RabbitMQ", flush=True)
        
        # GO BACK TO THIS - IT WAS WORKING!
        llm_response_consumer = LLMResponseConsumer(
            connection=connection,
            queue_name='llm-response-queue',
            callback_function=forward_result_to_websocket
        )
        print("Consumer created, starting consumption...", flush=True)
        
        llm_response_consumer.start_consuming()
    except Exception as e:
        print(f"Consumer thread failed: {e}", flush=True)
        import traceback
        traceback.print_exc()

def start_consumer_thread():
    """
    Starts the message queue consumer in a background thread.
    """
    print("=== STARTING CONSUMER THREAD ===", flush=True)
    try:
        loop = asyncio.get_event_loop()
        print(f"Got event loop: {loop}", flush=True)
        
        consumer_thread = threading.Thread(target=run_consumer, args=(loop,), daemon=True)
        consumer_thread.start()
        print("Consumer thread started successfully", flush=True)
    except Exception as e:
        print(f"Failed to start consumer thread: {e}", flush=True)
        import traceback
        traceback.print_exc()

main_event_loop = None
