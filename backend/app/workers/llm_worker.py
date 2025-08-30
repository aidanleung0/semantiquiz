import os
import json
import re
import pika
import threading
from pika.spec import PRECONDITION_FAILED
import openai
from message_queue.producers.message_producer import MessageProducer
from message_queue.consumers.llm_request_consumer import LLMRequestConsumer
from schemas.websocket_job import WebsocketResponse


def process_llm_batch(job_bodies: list, llm_client, result_producer):
    try:
        job_bodies = [json.loads(job_body.decode('utf-8')) for job_body in job_bodies]
    except json.JSONDecodeError as e:
        print(f"Error decoding job bodies: {e}", flush=True)
        return

    with open("prompts/llm_system_prompt.txt", "r") as f:
        system_prompt = f.read()
        prompt_items = []

    for job_body in job_bodies:
        item_string = (
            f"id: {job_body.get('job_id')}\n"
                f"- Word: {job_body.get('word')}\n"
                f"- User Definition: {job_body.get('user_input')}\n"
                f"- Canonical Definition: {job_body.get('ground_truth')}"
        )
        prompt_items.append(item_string)

    user_inputs = "\n\n".join(prompt_items)
    user_prompt = f"Please evaluate the following batch of user-submmitted vocabulary definitions.\n\nHere are the definitions to evaluate:\n---\n{user_inputs}"


    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = llm_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.1
        )

        response_content = response.choices[0].message.content
        job_map = {job['job_id']: job for job in job_bodies}

        batch_results = json.loads(response_content)

        for result in batch_results:
            job = job_map.get(result.get("id"))
            if job:
                print("job found", flush=True)
                
                # Add these debug prints
                print(f"Building payload for job {result.get('id')}", flush=True)
                
                result_payload = {
                    "status": "success",
                    "job_id": result.get("id"),
                    "word": result.get("word"),
                    "user_input": job.get("user_input"),
                    "ground_truth": job.get("ground_truth"),
                    "feedback": result.get("feedback"),
                    "example": result.get("example"),
                }
                
                print(f"Payload built: {result_payload}", flush=True)
                print(f"About to publish to llm-response-queue", flush=True)
                
                try:
                    result_producer.publish(queue_name='llm-response-queue', payload=result_payload)
                    print(f"Published successfully", flush=True)
                except Exception as e:
                    print(f"Publish failed: {e}", flush=True)
                    raise
        

    except Exception as e:
        print(f"An error occured during the batch LLM call: {e}", flush=True)

        for job_body in job_bodies:
            error_payload = {
                "status": "error",
                "job_id": job_body.get("job_id"),
                "feedback": "An error occured during the batch LLM call"
            }
            result_producer.publish(queue_name='llm-response-queue', payload=error_payload)

# def process_llm_job_callback(ch, method, properties, body, llm_client, result_producer):
#     print("Received new job from llm requests queue")
#     job_body = json.loads(body)
#
#     process_llm_batch([job_body], llm_client=llm_client, result_producer=result_producer)
#
#     ch.basic_ack(delivery_tag=method.delivery_tag)
#
#     print("Job finished and acknowledged")
#

if __name__ == "__main__":
    print("Worker startup...")

    try:
        llm_api_key = os.getenv("LLM_API_KEY")

        if not llm_api_key:
            raise ValueError("LLM_API_KEY not found in the environment")

        client = openai.OpenAI(
            api_key=llm_api_key,
            base_url="https://api.deepseek.com"
        )

        credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER", "guest"), os.getenv("RABBITMQ_PASS", "guest"))
        producer_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
        result_producer = MessageProducer(connection=producer_connection)

        on_message_callback = lambda job_bodies: process_llm_batch(job_bodies=job_bodies, llm_client=client, result_producer=result_producer)

        consumer_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
        llm_request_consumer = LLMRequestConsumer(
            connection=consumer_connection,
            queue_name='llm-request-queue',
            llm_process_function=on_message_callback
        )

        print("Worker is running and waiting for messages...", flush=True)

        consumer_thread = threading.Thread(target=llm_request_consumer.start_consuming, daemon=True)
        consumer_thread.start()
        consumer_thread.join()

    except Exception as e:
        print(f"An error occurred in the worker: {e}")
