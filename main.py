from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only; specify frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrackRequest(BaseModel):
    url: str


@app.get("/")
async def root():
    return {"message": "Reseller Backend Online"}


@app.post("/track")
async def tryTrack(payload: TrackRequest):
    return {"received_url": payload.url}