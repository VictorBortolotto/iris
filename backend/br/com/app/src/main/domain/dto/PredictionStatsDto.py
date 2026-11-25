from dataclasses import dataclass

@dataclass
class PredictionStatsDto:
  total_classifications: int
  setosa_count: int
  setosa_percentage: float
  versicolor_count: int
  versicolor_percentage: float
  virginica_count: int
  virginica_percentage: float