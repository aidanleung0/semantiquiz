from _typeshed import ExcInfo
from logging import error, exception
import os
import json
import pika
import openai
from dotenv import load_dotenv
from message_queue.producers.message_producer import MessageProducer
from message_queue.consumers.llm_request_consumer import LLMRequestConsumer
from schemas.websocket_job import WebsocketResponse


def process_llm_batch(job_bodies: list, llm_client, result_producer):
    with open("prompts/llm_system_prompt.txt", "r") as f:
        system_prompt = f.read()
        prompt_items = []

    for job_body in job_bodies:
        item_string = (
            f"Item {job_body.get('job_id')}"
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
            response_format={
                'type': 'json_object'
            }
        )

        batch_results = json.loads(response.choices[0].message.content)

        print(batch_results)

        job_map = {job['job_id']: job for job in job_bodies}

        for result in batch_results:
            job = job_map.get(result.get("job_id"))
            if job:
                result_payload = {
                    "status": "success",
                    "job_id": result.get("job_id"),
                    "word": result.get("word"),
                    "user_input": job.get("user_input"),
                    "ground_truth": job.get("ground_truth"),
                    "feedback": result.get("feedback"),
                    "example": result.get("example"),
                }
            result_producer.publish(queue_name='LLM-response-queue', payload=result_payload)

    except Exception as e:
        print(f"An error occured during the batch LLM call: {e}")

        for job_body in job_bodies:
            error_payload = {
                "status": "error",
                "job_id": job_body.get("job_id"),
                "feedback": "An error occured during the batch LLM call"
            }
            result_producer.publish(queue_name='LLM-response-queue', payload=error_payload)

def process_llm_job_callback(ch, method, properties, body, llm_client, result_producer):
    print("Received new job from llm requests queue")
    job_body = json.loads(body)

    process_llm_batch([job_body], llm_client=llm_client, result_producer=result_producer)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("Job finished and acknowledged")


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

        on_message_callback = lambda ch, method, properties, body: process_llm_job_callback(ch, method, properties, body, llm_client=client, result_producer=result_producer)

        consumer_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
        llm_request_consumer = LLMRequestConsumer(
            connection=consumer_connection,
            queue_name='LLM-request-queue',
            llm_process_function=on_message_callback
        )

        print("Worker is running and waiting for messages...")
        llm_request_consumer.start_consuming()

    except Exception as e:
        print(f"An error occurred in the worker: {e}")
