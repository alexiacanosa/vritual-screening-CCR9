from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from plapt import Plapt
import time


app = FastAPI()

plapt_model: Plapt = None
model_load_failed = False


class PredictionRequest(BaseModel):
    """Estructura esperada para la solicitud POST."""
    protein_sequence: str 
    ligand_smiles: str 



@app.post("/get_prediction", status_code=200)
async def get_prediction(data: PredictionRequest):
    """
    Ruta para recibir secuencias (proteína y ligando) y devolver la afinidad de unión predicha.
    """
    plapt_model = Plapt()
    
    if plapt_model is None:
        raise HTTPException(
            status_code=503, 
            detail="Servicio no disponible. El modelo PLAPT no se cargó correctamente al inicio."
        )

    try:
        results = plapt_model.predict_affinity(data.protein_sequence, data.ligand_smiles)
        return {"results":results}
        
    except Exception as e:
        print(f"Error interno durante la predicción: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error al procesar la predicción: {str(e)}"
        )

