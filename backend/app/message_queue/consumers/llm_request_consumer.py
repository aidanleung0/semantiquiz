from .base_consumer import BaseConsumer
import time

class LLMRequestConsumer(BaseConsumer):
    def __init__(self, connection, queue_name:str, llm_process_function, batch_size=5, rate_limit_seconds=1):
        super().__init__(connection, queue_name)
        self.batch_size = batch_size
        self.rate_limit_seconds = rate_limit_seconds
        self.llm_process_function = llm_process_function

    def start_consuming(self):
        while True:
            jobs_in_batch = []

            for _ in range(self.batch_size):
                method_frame, _, body = self.channel.basic_get(queue=self.queue_name)
                if body is None:
                    break
                print("Got a job", flush=True)
                jobs_in_batch.append({'method': method_frame, 'body': body})

            if jobs_in_batch:
                print(f"Processing a batch of {len(jobs_in_batch)} jobs.", flush=True)
                self.llm_process_function(job_bodies=list(map(lambda x: x['body'], jobs_in_batch)))

                for job in jobs_in_batch:
                    self.channel.basic_ack(delivery_tag=job['method'].delivery_tag)
            else:
                time.sleep(self.rate_limit_seconds)


