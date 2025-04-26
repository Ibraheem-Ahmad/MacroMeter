from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import food, auth, scale
from .config import settings

app = FastAPI(
    title="MacroMeter API",
    description="API for MacroMeter food tracking system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(food.router, prefix="/api/food", tags=["Food"])
app.include_router(scale.router, prefix="/api/scale", tags=["Scale"])

@app.get("/")
async def root():
    return {"message": "Welcome to MacroMeter API"} 