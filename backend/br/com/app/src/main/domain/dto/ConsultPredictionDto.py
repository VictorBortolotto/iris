from dataclasses import dataclass

@dataclass
class ConsultPredictionDto:
  id: int
  sepal_length: float
  sepal_width: float
  petal_length: float
  petal_width: float
  specie: str
  iris_setosa: float
  iris_versicolor: float
  iris_virginica: float
  query_date: str