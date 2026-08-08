from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import uvicorn
from typing import List
import httpx

app = FastAPI(title="Protein-Ligand Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def call_model(url: str, payload: dict):
    """Call external model service and return result"""
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url, json=payload, timeout=30.0)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise Exception(f"Model service error: {str(e)}")

class ProteinLigandPair(BaseModel):
    protein_sequence: str
    ligand_smiles: str

class PredictionRequest(BaseModel):
    data: List[ProteinLigandPair]
    options: List[str]

@app.post("/get_predictions", response_model=dict)
async def get_predictions(request: PredictionRequest):
    """Process protein-ligand pairs through 4 ML models in parallel"""
    if not request.data:
        raise HTTPException(status_code=400, detail="No data provided")
    
    results = []
    errors = []
    model1_results=[]
    model2_results=[]
    model3_results=[]
    model4_results=[]
    
    try:
        for i, pair in enumerate(request.data):
            try:
                payload = {
                    "protein_sequence": pair.protein_sequence,
                    "ligand_smiles": pair.ligand_smiles
                }
                
                model1_task = asyncio.create_task(
                    call_model("http://modelo1:5001/get_prediction", payload)
                )
                model2_task = asyncio.create_task(
                    call_model("http://modelo2:5002/get_prediction", payload)
                )
                model3_task = asyncio.create_task(
                    call_model("http://modelo3:5003/get_prediction", payload)
                )
                model4_task = asyncio.create_task(
                    call_model("http://modelo4:5004/get_prediction", payload)
                )
                
                model1_result, model2_result, model3_result, model4_result = await asyncio.gather(
                    model1_task, model2_task, model3_task, model4_task,
                    return_exceptions=True
                )
                
                errors_dict = {}
                
                if isinstance(model1_result, Exception):
                    model1_result = {"score": 0, "error": str(model1_result)}
                    errors_dict["model1"] = str(model1_result)
                elif not isinstance(model1_result, dict) or "score" not in model1_result:
                    errors_dict["model1"] = "Invalid response format"
                    
                if isinstance(model2_result, Exception):
                    model2_result = {"affinity": 0, "error": str(model2_result)}
                    errors_dict["model2"] = str(model2_result)
                elif not isinstance(model2_result, dict) or "affinity" not in model2_result:
                    errors_dict["model2"] = "Invalid response format"
                    
                if isinstance(model3_result, Exception):
                    model3_result = {"score": 0, "error": str(model3_result)}
                    errors_dict["model3"] = str(model3_result)
                elif not isinstance(model3_result, dict) or "score" not in model3_result:
                    errors_dict["model3"] = "Invalid response format"
                    
                if isinstance(model4_result, Exception):
                    model4_result = {"score": 0, "error": str(model4_result)}
                    errors_dict["model4"] = str(model4_result)
                elif not isinstance(model4_result, dict) or "score" not in model4_result:
                    errors_dict["model4"] = "Invalid response format"
                
                
                model1_results+=[model1_result["score"]]
                model2_results+=[model2_result["affinity"]]
                model3_results+=[model3_result["score"]]
                model4_results+=[model4_result["score"]]


                result = {
                    "protein_sequence": pair.protein_sequence,
                    "ligand_smiles": pair.ligand_smiles,
                    "model1_result": model1_result,
                    "model2_result": model2_result,
                    "model3_result": model3_result,
                    "model4_result": model4_result,
                    "weighted_ranking": None,
                    "status": "success" if not errors_dict else "partial_success"
                }
                results.append(result)
                
            except Exception as e:
                error_result = {
                    "protein_sequence": pair.protein_sequence,
                    "ligand_smiles": pair.ligand_smiles,
                    "error": str(e),
                    "status": "error"
                }
                results.append(error_result)
                errors.append(f"Row {i}: {str(e)}")

        

        model1_results_total=sum(model1_results)
        model1_normalized_res=[result/model1_results_total if model1_results_total!=0 else 0 for result in model1_results]

        model2_results_total=sum(model2_results)
        model2_normalized_res=[result/model2_results_total if model2_results_total!=0 else 0 for result in model2_results]

        model3_results_total=sum(model3_results)
        model3_normalized_res=[result/model3_results_total if model3_results_total!=0 else 0 for result in model3_results]

        model4_results_total=sum(model4_results)
        model4_normalized_res=[result/model4_results_total if model4_results_total!=0 else 0 for result in model4_results]
        
        valor_ranking=[]
        for elemento in zip(model1_normalized_res,model2_normalized_res,model3_normalized_res,model4_normalized_res):
            valor_ranking.append(sum(elemento))
        
        for i in range(len(results)):
            results[i]["weighted_ranking"]=valor_ranking[i]
            

        return {
            "status": "completed",
            "total_processed": len(request.data),
            "successful": len([r for r in results if r.get("status") == "success"]),
            "partial_success": len([r for r in results if r.get("status") == "partial_success"]),
            "errors": len(errors),
            "results": results,
            "error_details": errors if errors else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
