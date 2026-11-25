
import importlib
from unittest.mock import Mock

import pytest
from flask import Flask

from controller.PredictionController import PredictionController


@pytest.fixture
def controller_client(monkeypatch):
  controller_module = importlib.import_module(
    "controller.PredictionController"
  )

  # Mock do carregamento do modelo
  model = Mock()
  load_model_mock = Mock()
  load_model_mock.load_model.return_value = model

  # Mock dos serviços
  prediction_service = Mock()
  find_all_service = Mock()
  find_by_id_service = Mock()
  stats_service = Mock()

  # Substituindo as dependências do Controller
  monkeypatch.setattr(
    controller_module,
    "LoadModel",
    Mock(return_value=load_model_mock)
  )

  monkeypatch.setattr(
    controller_module,
    "PredictionService",
    Mock(return_value=prediction_service)
  )

  monkeypatch.setattr(
    controller_module,
    "FindAllPredictionService",
    Mock(return_value=find_all_service)
  )

  monkeypatch.setattr(
    controller_module,
    "FindPredictionByIdService",
    Mock(return_value=find_by_id_service)
  )

  monkeypatch.setattr(
    controller_module,
    "PredictionStatService",
    Mock(return_value=stats_service)
  )

  # Aplicação Flask isolada para os testes
  app = Flask(__name__)
  app.testing = True

  controller = PredictionController(app)

  return {
    "client": app.test_client(),
    "controller": controller,
    "model": model,
    "prediction_service": prediction_service,
    "find_all_service": find_all_service,
    "find_by_id_service": find_by_id_service,
    "stats_service": stats_service
  }


def test_classify_route_success(controller_client):
  client = controller_client["client"]
  model = controller_client["model"]
  prediction_service = controller_client["prediction_service"]

  request_data = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }

  expected_result = {
    "species": "Iris Setosa",
    "probabilities": {
      "Iris Setosa": 0.90,
      "Iris Versicolor": 0.05,
      "Iris Virginica": 0.05
    }
  }

  prediction_service.predict_species.return_value = expected_result

  response = client.post(
    "/prediction/predict",
    json=request_data
  )

  prediction_service.predict_species.assert_called_once_with(
    model,
    request_data
  )

  assert response.status_code == 200
  assert response.get_json() == expected_result


def test_find_all_prediction_route_success(controller_client):
  client = controller_client["client"]
  find_all_service = controller_client["find_all_service"]

  expected_result = {
    "message": "Predictions retrieved successfully."
  }

  find_all_service.find_all_prediction.return_value = expected_result

  response = client.get("/prediction/all")

  find_all_service.find_all_prediction.assert_called_once_with(None)

  assert response.status_code == 200
  assert response.get_json() == expected_result


def test_find_all_prediction_with_specie_filter(controller_client):
  client = controller_client["client"]
  find_all_service = controller_client["find_all_service"]

  expected_result = {
    "message": "Predictions retrieved successfully."
  }

  find_all_service.find_all_prediction.return_value = expected_result

  response = client.get("/prediction/all?specie=setosa")

  find_all_service.find_all_prediction.assert_called_once_with("setosa")

  assert response.status_code == 200
  assert response.get_json() == expected_result


def test_find_prediction_by_id_route_success(controller_client):
  client = controller_client["client"]
  find_by_id_service = controller_client["find_by_id_service"]

  expected_result = {
    "message": "Prediction retrieved successfully."
  }

  find_by_id_service.find_prediction_by_id.return_value = expected_result

  response = client.get("/prediction/10")

  find_by_id_service.find_prediction_by_id.assert_called_once_with("10")

  assert response.status_code == 200
  assert response.get_json() == expected_result


def test_prediction_stats_route_success(controller_client):
  client = controller_client["client"]
  stats_service = controller_client["stats_service"]

  expected_result = {
    "total_predictions": 150,
    "setosa": 50,
    "versicolor": 50,
    "virginica": 50
  }

  stats_service.prediction_stats.return_value = expected_result

  response = client.get("/prediction/stats")

  stats_service.prediction_stats.assert_called_once()

  assert response.status_code == 200
  assert response.get_json() == expected_result
