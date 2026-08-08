from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from plapt import Plapt
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    global plapt
    try:
        plapt = await asyncio.to_thread(Plapt)
        print("PLAPT model initialized successfully")
    except Exception as e:
        print(f"Failed to initialize PLAPT: {e}")
        plapt = None

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

plapt = None



class PredictionRequest(BaseModel):
    protein_sequence: str
    ligand_smiles: str

@app.post("/get_prediction")
async def get_prediction(data: PredictionRequest):
    global plapt

    if plapt is None:
        raise HTTPException(500, "Model not loaded yet")

    affinities = plapt.score_candidates(
        data.protein_sequence,
        [data.ligand_smiles]
    )
    return {"affinity": affinities[0]["affinity_uM"]}

@app.get("/health")
async def health():
    return {"status": "ok" if plapt is not None else "loading"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
