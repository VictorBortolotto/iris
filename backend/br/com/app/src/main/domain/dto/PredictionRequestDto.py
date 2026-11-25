from dataclasses import dataclass
from pydantic import Field

@dataclass
class PredictionRequestDto:
  sepal_length: float = Field(gt=0)
  sepal_width: float = Field(gt=0)
  petal_length: float = Field(gt=0)
  petal_width: float = Field(gt=0)