# semantiquiz
## How to Run/Test the Backend
### Prerequisites
1. Add `LLM_API_KEY`, `RABBITMQ_USER`, and `RABBITMQ_PASS` to a `.env` file and put it in the root directory.<br>
It should look something like this:
   ```.env
   LLM_API_KEY=your-llm-api-key
   RABBITMQ_USER=arbitrary-user
   RABBITMQ_PASS=arbitrary-password
2. Make sure you have `docker` installed
3. Make sure you have `websocat` installed, or any tool that can send websocket requests
### Run the Backend
1. `cd backend/`
2. Run `sudo docker-compose up --build -d` if you're running for the first time,<br>
otherwise just run `sudo docker-compose up -d`
3. Send an HTTP request with curl (below is an example request):
   ```bash
   curl -X POST "http://localhost:8000/api/compare-definition" \
   -H "Content-Type: application/json" \
   -d '{
      "word": "ephemeral",
      "user_input": "Something that is temporary and does not last long.",
      "ground_truth": "Lasting for a very short time."
   }'
4. After you get the `job_id`, run the websocket request with `websocat`
5. Send a websocket request with `websocat` (below is an example request):
   ```bash
   websocat ws://localhost:8000/api/ws/YOUR_JOB_ID_HERE
