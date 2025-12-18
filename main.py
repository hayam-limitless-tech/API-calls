from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import uuid

app = FastAPI()
jobs: dict[str, float] = {}

class StatusRequest(BaseModel):
    job_id: str

@app.post("/start")
def start_job():
    job_id = str(uuid.uuid4())
    jobs[job_id] = time.time()
    return {
        "job_id": job_id,
        "status": "pending"
    }

@app.post("/status")
def get_status(body: StatusRequest):
    start_time = jobs.get(body.job_id)

    if start_time is None:
        raise HTTPException(status_code=404, detail="job not found")

    elapsed = time.time() - start_time

    if elapsed >= 120:
        return {
            "job_id": body.job_id,
            "status": "completed"
        }

    return {
        "job_id": body.job_id,
        "status": "pending",
        "seconds_remaining": int(120 - elapsed)
    }
