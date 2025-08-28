from contextlib import asynccontextmanager
from message_queue.producers.message_producer import MessageProducer
from fastapi import FastAPI
from routes.http_routes import evaluation
from routes.websocket_routes import job_websocket
from routes.websocket_routes import test_websocket
from workers.websocket_handler import start_consumer_thread
import pika
import os


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Connecting to RabbitMQ...")
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER", "guest"), os.getenv("RABBITMQ_PASS", "guest"))
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
    producer = MessageProducer(connection=connection)
    app.state.producer = producer
    print("Connection successful, publisher is ready.")

    print("Starting message queue consumer thread")
    start_consumer_thread()
    print("Consumer thread started.")

    yield

    print("Closing RabbitMQ connection...")
    app.state.producer.close_connection()
    print("Connection closed")

app = FastAPI(lifespan=lifespan)

app.include_router(evaluation.router, prefix="/api")
app.include_router(job_websocket.router, prefix="/api/ws")
app.include_router(test_websocket.router, prefix="/api/ws")

@app.get("/")
async def root():
    return {"message": "Hello World"}


