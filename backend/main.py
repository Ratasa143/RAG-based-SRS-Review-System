from fastapi import FastAPI
from api import upload, analyze

app = FastAPI(title="SRS Review System")

app.include_router(upload.router)
app.include_router(analyze.router)

@app.get("/health")
def health():
    return {"status": "ok"}
