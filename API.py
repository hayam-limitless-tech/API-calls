from fastapi import FastAPI
import time
import uuid

app = FastAPI()

jobs = {}

@app.post("/start")
def start_job():
    job_id = str(uuid.uuid4())
    jobs[job_id] = time.time()
    return {
        "job_id": job_id,
        "status": "pending"
    }

@app.get("/status/{job_id}")
def get_status(job_id: str):
    start_time = jobs.get(job_id)

    if not start_time:
        return {"error": "job not found"}

    elapsed = time.time() - start_time

    if elapsed >= 120:
        return {
            "job_id": job_id,
            "status": "completed"
        }

    return {
        "job_id": job_id,
        "status": "pending",
        "seconds_remaining": int(120 - elapsed)
    }
