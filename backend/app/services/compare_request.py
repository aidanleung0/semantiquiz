from schemas.compare import CompareResponse
from uuid import uuid4
from message_queue.producers.message_producer import MessageProducer

def compare_request(producer, payload):
    # Push a new job to message queue
    job_id = uuid4()

    data_to_send = {
        "job_id": job_id,
        **payload
    }

    producer.publish(queue_name='llm-request-queue', payload=data_to_send)

    # Return job_id
    return CompareResponse(
        job_id=str(job_id)
    )
