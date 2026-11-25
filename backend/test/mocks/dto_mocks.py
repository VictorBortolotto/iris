
from domain.dto.ConsultPredictionDto import ConsultPredictionDto
from domain.dto.PredictionRequestDto import PredictionRequestDto
from domain.dto.PredictionResponseDto import PredictionResponseDto
from domain.dto.PredictionStatsDto import PredictionStatsDto


def mock_consult_prediction():
  return ConsultPredictionDto(
    id=1,
    sepal_length=5.1,
    sepal_width=3.5,
    petal_length=1.4,
    petal_width=0.2,
    specie="setosa",
    iris_setosa=0.95,
    iris_versicolor=0.03,
    iris_virginica=0.02,
    query_date="2026-11-25 10:30:00"
  )


def mock_prediction_request():
  return PredictionRequestDto(
    sepal_length=5.1,
    sepal_width=3.5,
    petal_length=1.4,
    petal_width=0.2
  )


def mock_prediction_response():
  return PredictionResponseDto(
    species="setosa",
    probabilities={
      "setosa": 0.95,
      "versicolor": 0.03,
      "virginica": 0.02
    }
  )


def mock_prediction_stats():
  return PredictionStatsDto(
    total_classifications=100,
    setosa_count=40,
    setosa_percentage=40.0,
    versicolor_count=35,
    versicolor_percentage=35.0,
    virginica_count=25,
    virginica_percentage=25.0
  )
