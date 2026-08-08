from model1 import *
import torch
from torch_geometric.data import Data
from rdkit import Chem
import numpy as np
import networkx as nx
from gnn import GNNNet  
import warnings
warnings.filterwarnings("ignore")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import time

model: GNNNet = None
model_load_failed = False


class PredictionRequest(BaseModel):
    protein_sequence: str 
    ligand_smiles: str 

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, model_load_failed
    start_time = time.time()
    
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_path = "model_GNNNet_davis.model"
        model = load_model(model_path, device)
        
    except Exception as e:
        end_time = time.time()
        print(f"Error CRÍTICO al inicializar el modelo1 después de {end_time - start_time:.2f} segundos: {e}")
        model_load_failed = True
    yield
    model.clear()

app = FastAPI(
    lifespan=lifespan,
    title="Modelo1 Prediction API",
    description="API para predicción de afinidad proteína-ligando usando el modelo1."
)


@app.post("/get_prediction", status_code=200)
async def get_prediction(data: PredictionRequest):

    mol_graph = mol_to_graph_features(data.ligand_smiles)
    pro_graph = seq_feature(data.protein_sequence)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = "model_GNNNet_davis.model"
    model = load_model(model_path, device)

    mol_graph = mol_graph.to(device)
    pro_graph = pro_graph.to(device)

    with torch.no_grad():
        pred = model(mol_graph, pro_graph)
    
    pKd = pred
    Kd = 10**(-pKd)                  # M

    return {
        "score": float(pred),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
