from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import records

app = FastAPI(title="SWRIA Quantum-Link Registry API", version="1.0")

# CORS (restringir en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar por el dominio de Vercel en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records.router)

@app.get("/")
async def root():
    return {"message": "SWRIA Quantum-Link Registry API", "status": "operational"}
