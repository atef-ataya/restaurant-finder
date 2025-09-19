from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
from crew import SimpleRestaurantFinder

app = FastAPI(title="Restaurant Finder API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

executor = ThreadPoolExecutor(max_workers=2)

class Query(BaseModel):
    query: str
    location: Optional[str] = "San Francisco"

@app.get("/")
def home():
    return {"message": "Restaurant Finder API 🍽️"}

@app.post("/find-restaurants")
async def find_restaurants(query: Query):
    """Find restaurants endpoint"""
    def run_finder():
        finder = SimpleRestaurantFinder()
        return finder.run(query.location)
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, run_finder)
    
    return {
        "location": query.location,
        "recommendations": str(result)
    }

@app.post("/query")
async def copilot_query(query: Query):
    """CopilotKit compatible endpoint"""
    def run_finder():
        finder = SimpleRestaurantFinder()
        return finder.run(query.location)
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, run_finder)
    
    return {
        "generateCopilotResponse": {
            "messages": [
                {
                    "content": str(result),
                    "role": "assistant"
                }
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)