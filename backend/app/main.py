from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from .models import MatrixConfig, FitRequest, FitResponse
from .geometry import fit_contain
from .importers import inspect_upload, MAX_BYTES

app = FastAPI(title="LaserCraft Studio", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.1.0", "sprint": 0}


@app.get("/api/matrix/default")
def default_matrix():
    config = MatrixConfig()
    return {**config.model_dump(), "usable_width_mm": config.usable_width_mm,
            "usable_height_mm": config.usable_height_mm}


@app.post("/api/geometry/fit", response_model=FitResponse)
def fit_image(request: FitRequest):
    return fit_contain(request)


@app.post("/api/import/inspect")
async def inspect_image(file: UploadFile = File(...)):
    try:
        data = await file.read(MAX_BYTES + 1)
        return inspect_upload(file.filename or "", data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        await file.close()
