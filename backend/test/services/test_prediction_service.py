
from unittest.mock import Mock, patch
from datetime import datetime

import numpy as np
import pandas as pd

from services.PredictionService import PredictionService


def test_predict_species_success():
  request = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }

  model = Mock()
  model.predict.return_value = np.array([0])
  model.predict_proba.return_value = np.array([[0.90, 0.05, 0.05]])
  model.classes_ = np.array([0, 1, 2])

  id_request = 10

  with patch(
    "services.PredictionService.PredictionRepository"
  ) as repository_mock:

    repository_mock.return_value.insert_request_data.return_value = id_request

    service = PredictionService()

    result = service.predict_species(model, request)

  repository_mock.return_value.insert_request_data.assert_called_once_with(request)

  repository_mock.return_value.insert_query_data.assert_called_once()

  args = repository_mock.return_value.insert_query_data.call_args[0]

  assert args[0] == "Iris Setosa"
  assert args[1] == 0.90
  assert args[2] == 0.05
  assert args[3] == 0.05
  assert isinstance(args[4], datetime)
  assert args[5] == id_request

  expected_data = pd.DataFrame(
    [[5.1, 3.5, 1.4, 0.2]],
    columns=service.FEATURE_NAMES
  )

  pd.testing.assert_frame_equal(
    model.predict.call_args[0][0],
    expected_data
  )

  assert result["species"] == "Iris Setosa"

  assert result["probabilities"] == {
    "Iris Setosa": 0.90,
    "Iris Versicolor": 0.05,
    "Iris Virginica": 0.05
  }


def test_predict_species_versicolor():
  request = {
    "sepal_length": 6.0,
    "sepal_width": 2.7,
    "petal_length": 4.5,
    "petal_width": 1.5
  }

  model = Mock()
  model.predict.return_value = np.array([1])
  model.predict_proba.return_value = np.array([[0.10, 0.80, 0.10]])
  model.classes_ = np.array([0, 1, 2])

  with patch(
    "services.PredictionService.PredictionRepository"
  ) as repository_mock:

    repository_mock.return_value.insert_request_data.return_value = 20

    service = PredictionService()

    result = service.predict_species(model, request)

  assert result["species"] == "Iris Versicolor"

  assert result["probabilities"]["Iris Setosa"] == 0.10
  assert result["probabilities"]["Iris Versicolor"] == 0.80
  assert result["probabilities"]["Iris Virginica"] == 0.10


def test_predict_species_virginica():
  request = {
    "sepal_length": 6.3,
    "sepal_width": 3.3,
    "petal_length": 6.0,
    "petal_width": 2.5
  }

  model = Mock()
  model.predict.return_value = np.array([2])
  model.predict_proba.return_value = np.array([[0.05, 0.05, 0.90]])
  model.classes_ = np.array([0, 1, 2])

  with patch(
    "services.PredictionService.PredictionRepository"
  ) as repository_mock:

    repository_mock.return_value.insert_request_data.return_value = 30

    service = PredictionService()

    result = service.predict_species(model, request)

  assert result["species"] == "Iris Virginica"

  assert result["probabilities"]["Iris Setosa"] == 0.05
  assert result["probabilities"]["Iris Versicolor"] == 0.05
  assert result["probabilities"]["Iris Virginica"] == 0.90
