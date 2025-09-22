from contextlib import asynccontextmanager
from message_queue.producers.message_producer import MessageProducer

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from workers.websocket_handler import start_consumer_thread
from app.router import api_router
from app.core.config import settings

import pika
import os


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Connecting to RabbitMQ...")
    # credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER", "guest"), os.getenv("RABBITMQ_PASS", "guest"))
    # connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
    producer = MessageProducer()
    app.state.producer = producer
    print("Connection successful, publisher is ready.")

    print("Starting message queue consumer thread")
    start_consumer_thread()
    print("Consumer thread started.")

    yield

    print("Shutdown complete.")
    # print("Closing RabbitMQ connection...")
    # app.state.producer.close_connection()
    # print("Connection closed")

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


