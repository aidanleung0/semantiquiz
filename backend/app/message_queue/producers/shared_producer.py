# backend/app/message_queue/producers/shared_producer.py
import os
import pika
import json
import threading
import time
import logging

def _rabbit_params():
    url = os.getenv("RABBITMQ_URL")
    if url:
        return pika.URLParameters(url)  # keep broker defaults; no heartbeat changes
    return pika.ConnectionParameters(
        'rabbitmq',
        credentials=pika.PlainCredentials(os.getenv("RABBITMQ_USER", "guest"), os.getenv("RABBITMQ_PASS", "guest")),
        # no heartbeat override
    )

class SharedConnectionProducer:
    def __init__(self, parameters: pika.ConnectionParameters | pika.URLParameters | None = None):
        self.parameters = parameters or _rabbit_params()
        self._conn = None
        self._ch = None
        self._lock = threading.Lock()
        self._keepalive_thread = None
        self._stop_evt = threading.Event()

    def _connect(self):
        if self._conn and self._conn.is_open and self._ch and self._ch.is_open:
            return
        # (Re)connect
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
        self._conn = pika.BlockingConnection(self.parameters)
        self._ch = self._conn.channel()
        logging.info("SharedConnectionProducer connected")

    def start(self):
        # establish connection
        with self._lock:
            self._connect()
        # start keepalive thread
        self._stop_evt.clear()
        self._keepalive_thread = threading.Thread(target=self._keepalive_loop, daemon=True)
        self._keepalive_thread.start()

    def close(self):
        self._stop_evt.set()
        if self._keepalive_thread:
            self._keepalive_thread.join(timeout=5)
        with self._lock:
            try:
                if self._ch and self._ch.is_open:
                    self._ch.close()
            except Exception:
                pass
            try:
                if self._conn and self._conn.is_open:
                    self._conn.close()
            except Exception:
                pass
            self._conn = None
            self._ch = None

    def _keepalive_loop(self):
        # Drive heartbeats and detect drops; reconnect if needed.
        while not self._stop_evt.is_set():
            try:
                with self._lock:
                    if not (self._conn and self._conn.is_open):
                        self._connect()
                    # process data events for a short time to send/receive heartbeats
                    self._conn.process_data_events(time_limit=0.2)
            except Exception as e:
                logging.warning(f"Keepalive loop detected connection issue: {e}. Reconnecting soon...")
                time.sleep(1.0)  # brief backoff
                try:
                    with self._lock:
                        self._connect()
                except Exception:
                    time.sleep(2.0)
            finally:
                time.sleep(1.0)  # keepalive tick

    def publish(self, queue_name: str, payload: dict):
        body = json.dumps(payload)
        with self._lock:
            try:
                self._connect()
                self._ch.queue_declare(queue=queue_name, durable=True)
                self._ch.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=body,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
            except (pika.exceptions.AMQPError, OSError) as e:
                # try one reconnect + retry
                logging.warning(f"Publish failed, retrying once: {e}")
                self._connect()
                self._ch.queue_declare(queue=queue_name, durable=True)
                self._ch.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=body,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
