import os
import sys

from transformers import AutoTokenizer
import torch
from datasets import load_dataset

import time
import common_utils
from balm.models.utils import load_trained_model, load_pretrained_pkd_bounds
from balm.configs import Configs
from balm.models import BALM
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
    global model,protein_tokenizer,drug_tokenizer,pkd_lower_bound,pkd_upper_bound
    config_filepath = "default_configs/balm_peft.yaml"
    configs = Configs(**common_utils.load_yaml(config_filepath))

    try:
        model = BALM(configs.model_configs)
        model = load_trained_model(model, configs.model_configs, is_training=False)
        model.to(DEVICE)
        model.eval()

        # Pretrained pKd lower and upper bounds
        pkd_lower_bound, pkd_upper_bound = load_pretrained_pkd_bounds(configs.model_configs.checkpoint_path)

        # Load the tokenizers
        protein_tokenizer = AutoTokenizer.from_pretrained(
            configs.model_configs.protein_model_name_or_path
            )

        drug_tokenizer = AutoTokenizer.from_pretrained(
            configs.model_configs.drug_model_name_or_path
            )

    except Exception as e:
        print(f"Error CRÍTICO al inicializar el modelo4")

    yield
    model.clear()




DEVICE = "cpu"

app= FastAPI(lifespan=lifespan)

class PredictionRequest(BaseModel):
    protein_sequence: str 
    ligand_smiles: str 


@app.post("/get_prediction", status_code=200)
async def get_prediction(data: PredictionRequest):
    protein_inputs = protein_tokenizer(data.protein_sequence, return_tensors="pt").to(DEVICE)
    drug_inputs = drug_tokenizer(data.ligand_smiles, return_tensors="pt").to(DEVICE)

    inputs = {
            "protein_input_ids": protein_inputs["input_ids"],
            "protein_attention_mask": protein_inputs["attention_mask"],
            "drug_input_ids": drug_inputs["input_ids"],
            "drug_attention_mask": drug_inputs["attention_mask"],
        }

    prediction = model(inputs)["cosine_similarity"]
    prediction = model.cosine_similarity_to_pkd(prediction, pkd_upper_bound=pkd_upper_bound, pkd_lower_bound=pkd_lower_bound)

    return {
        "score":float(prediction),
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5004)