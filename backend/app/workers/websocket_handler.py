import pika
import json
import threading
import asyncio
from message_queue.consumers.llm_response_consumer import LLMResponseConsumer
from connection_manager import connection_manager

def forward_result_to_websocket(body):
    """
    Callback function for the message queue consumer
    """
    try:
        data = json.loads(body)
        job_id = data.get("job_id")

        if job_id:
            asyncio.run_coroutine_threadsafe(
                connection_manager.send_message(job_id, data),
                main_event_loop
            )
        else:
            print("Warning: Received a message without a job_id.")

    except Exception as e:
        print(f"An error occurred in the handler callback: {e}")

def run_consumer(loop):
    """
    Sets up the message queue consumer and assigns the main event loop.
    """
    global main_event_loop
    main_event_loop = loop
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    llm_response_consumer = LLMResponseConsumer(
        connection=connection,
        queue_name='LLM-response-queue',
        callback_function=forward_result_to_websocket
    )

    llm_response_consumer.start_consuming()

def start_consumer_thread():
    """
    Starts the message queue consumer in a background thread.
    """
    loop = asyncio.get_event_loop()

    consumer_thread = threading.Thread(target=run_consumer, args=(loop,), daemon=True)
    consumer_thread.start()

main_event_loop = None
