from fastapi import FastAPI
from pydantic import BaseModel
from optimiser import optimise_plan
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Plan Optimiser API",
    description="Backend API for RAG-powered AI plan optimiser",
    version="1.0"
)

# Allow frontend or local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request format
class PlanRequest(BaseModel):
    plan: str

# Root endpoint
@app.get("/")
def home():
    return {"message": "AI Plan Optimiser Backend Running"}

# Main optimisation endpoint
@app.post("/optimise_plan")
def optimise(request: PlanRequest):
    result = optimise_plan(request.plan)
    return result

