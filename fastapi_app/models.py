# fastapi_app/models.py
from pydantic import BaseModel

class PredictionResult(BaseModel):
    category: str
    material: str
    color: str
