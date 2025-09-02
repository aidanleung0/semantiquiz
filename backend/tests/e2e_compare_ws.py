import asyncio
import json
import websockets
import httpx

API = "http://localhost:8000"
WS = "ws://localhost:8000"

async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        payload = {
            "word": "matcha",
            "ground_truth": "a finely ground powder of specially grown and processed green tea leaves",
            "user_input": "a type of green tea powder"
        }
        resp = await client.post(f"{API}/api/compare-definition", json=payload)
        resp.raise_for_status()
        job = resp.json()
        job_id = job["job_id"]
        print("job_id:", job_id)

    # Connect websocket after you have the job_id; server will buffer messages if worker was faster
    async with websockets.connect(f"{WS}/api/ws/{job_id}") as ws:
        msg = await asyncio.wait_for(ws.recv(), timeout=30)
        data = json.loads(msg) if isinstance(msg, str) else msg
        print("WS message:", data)

        # Minimal schema checks – adjust to your worker’s payload
        assert data["job_id"] == job_id
        assert data["status"] == "success"
        assert data["word"] == payload["word"]
        assert data["user_input"] == payload["user_input"]
        assert data["ground_truth"] == payload["ground_truth"]
        assert data["feedback"] is not None
        assert data["example"] is not None

if __name__ == "__main__":
    asyncio.run(main())