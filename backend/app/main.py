from contextlib import asynccontextmanager
from app.message_queue.producers.message_producer import MessageProducer
from fastapi import FastAPI
from routes.http_routes import evaluation
from routes.websocket_routes import job_websocket
from workers.websocket_handler import start_consumer_thread
import pika

app = FastAPI()

app.include_router(evaluation.router, prefix="/api")
app.include_router(job_websocket.router, prefix="/api/ws")

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Connecting to RabbitMQ...")
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    publisher = MessageProducer(connection=connection)
    app.state.publisher = publisher
    print("Connection successful, publisher is ready.")

    yield

    print("Closing RabbitMQ connection...")
    app.state.publisher.close_connection()
    print("Connection closed")

@app.on_event("startup")
def startup_event():
    print("Application is starting up...")
    start_consumer_thread()
    print("Message queue consumer thread has been started in the background.")


@app.get("/")
async def root():
    return {"message": "Hello World"}
