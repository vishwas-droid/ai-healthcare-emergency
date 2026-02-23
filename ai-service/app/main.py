from fastapi import FastAPI
from pydantic import BaseModel

from app.triage_llm import triage_llm

app = FastAPI(title="AI Triage Service")


class TriagePayload(BaseModel):
    complaint_text: str


@app.get("/")
def health():
    return {"status": "ok", "service": "ai-triage"}


@app.post("/triage")
def triage(payload: TriagePayload):
    return triage_llm(payload.complaint_text)
