from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class PredictionResponseDto(BaseModel):
  species: str
  probabilities: dict[str, float]