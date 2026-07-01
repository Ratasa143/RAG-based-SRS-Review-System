from fastapi import FastAPI
from api import upload, analyze
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SRS Review System")
# Enable CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(upload.router)
app.include_router(analyze.router)

@app.get("/")
def root():
    return {
        "message": "SRS Review System Backend Running"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
