from fastapi import FastAPI
from routes import evaluation

app = FastAPI()

app.include_router(evaluation.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}