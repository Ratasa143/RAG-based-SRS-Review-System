from fastapi import FastAPI
from api import upload, analyze

app = FastAPI(title="SRS Review System")

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
