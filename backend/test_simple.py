"""
Test básico de FastAPI para Recuiva
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Recuiva Test")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Recuiva Backend Test - OK"}

@app.get("/api/materials")
async def get_materials():
    return {
        "materials": [],
        "total": 0
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
