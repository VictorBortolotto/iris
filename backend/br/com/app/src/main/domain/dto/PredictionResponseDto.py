from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class PredictionResponse(BaseModel):
  species: str
  probabilities: dict[str, float]