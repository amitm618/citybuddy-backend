from fastapi import FastAPI, Query
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


PLACES_API_KEY = os.getenv("PLACES1_API_KEY")

@app.get("/recommendations")
def get_recommendations(
    lat: float = Query(...),
    lng: float = Query(...),
    type: str = Query(default="restaurant")
):
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}&radius=1500&type={type}&key={PLACES_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    results = [
        {
            "name": place.get("name"),
            "rating": place.get("rating"),
            "address": place.get("vicinity"),
            "open_now": place.get("opening_hours", {}).get("open_now", "N/A")
        }
        for place in data.get("results", [])
    ]
    return {"results": results}