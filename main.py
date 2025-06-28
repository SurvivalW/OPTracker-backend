import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bs4 import BeautifulSoup
from fastapi import HTTPException


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://survivalw.github.io"],  # GitHub Pages domain
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
    url = payload.url

    if "amazon." not in url:
        raise HTTPException(status_code=400, detail="Only Amazon URLs for now.")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch URL: {e}")
    
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "Title not found XD"

    price_tag = (
        soup.find(id="priceblock_ourprice")
        or soup.find(id="priceblock_dealprice")
        or soup.find("span", class_="a-offscreen")
    )
    price = price_tag.get_text(strip=True) if price_tag else "Price not found XD"

    availability_tag = soup.find(id="availability")
    availability = availability_tag.get_text(strip=True) if availability_tag else "Unknown"

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "url": url,
    }