from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from agent import CryptoAgent
import uvicorn
import os

app = FastAPI(
    title="AI Crypto Agent API",
    description="Backend for the 3D AI Crypto Agent Experience"
)

print("\n" + "="*50)
print("   AI CRYPTO AGENT SERVER IS STARTING")
print("="*50)
print("[NOTE] If you see 'Pizza Palace' errors, please close")
print("       other browser tabs from previous projects.\n")


# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
agent = CryptoAgent()

class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    response: str
    icon_url: str = ""

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        response_text = agent.process_query(request.prompt)
        # Get icon for the last resolved symbol in agent context
        symbol = agent.context.last_symbol
        coin_data = agent.kb.get_coin_data(symbol) if symbol else None
        icon_url = coin_data.get("icon_url", "") if coin_data else ""
        
        return QueryResponse(response=response_text, icon_url=icon_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/media/{query}")
async def get_media(query: str):
    metadata = agent.get_image_metadata(query)
    return metadata

# Mount static files (MUST BE LAST to avoid shadowing API routes)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    print(f"[System] Serving frontend from: {frontend_path}")
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"[Warning] Frontend directory not found at: {frontend_path}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
