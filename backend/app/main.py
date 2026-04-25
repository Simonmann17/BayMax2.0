from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.routes import auth

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BayMax Symptom Checker,"
    "A triage system that evaluates symptoms and provides urgency levels and recommendations.",
    version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/")
def root(): 
    return {"message": "Welcome to the BayMax Symptom Checker API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
