from DeepPurpose import DTI as models
from DeepPurpose import utils

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import warnings
warnings.filterwarnings("ignore")


model=None
protein_tokenizer=None
drug_tokenizer=None
pkd_lower_bound,pkd_upper_bound= None,None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    try:
        MODEL_NAME = "MPNN_CNN_BindingDB"
        model = models.model_pretrained(model=MODEL_NAME)

    except Exception as e:
        print(f"Error CRÍTICO al inicializar el modelo4")

    yield
    model.clear()


app= FastAPI(lifespan=lifespan)

class PredictionRequest(BaseModel):
    protein_sequence: str 
    ligand_smiles: str 


@app.post("/get_prediction", status_code=200)
async def get_prediction(data: PredictionRequest):

    X_drug = [data.ligand_smiles]
    X_target = [data.protein_sequence]
    y = [0] 

    X_drug, X_target, _ = utils.data_process(
        X_drug,
        X_target,
        y=y,
        drug_encoding="MPNN",
        target_encoding="CNN"
    )
    pred = model.predict(X_drug)   

    return {
        "score":float(pred[0]),
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003)