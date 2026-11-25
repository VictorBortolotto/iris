
from unittest.mock import patch

from services.PredictionStatService import PredictionStatService


def test_prediction_stats_success(app_context):
    stats = {
        "total_predictions": 150,
        "setosa": 50,
        "versicolor": 50,
        "virginica": 50
    }

    with patch(
        "services.PredictionStatService.PredictionRepository"
    ) as repository_mock:

        repository_mock.return_value.prediction_stats.return_value = stats

        service = PredictionStatService()

        result = service.prediction_stats()

    repository_mock.return_value.prediction_stats.assert_called_once()

    assert result is not None
    assert result[1] == 200


def test_prediction_stats_empty_result(app_context):
    stats = {}

    with patch(
        "services.PredictionStatService.PredictionRepository"
    ) as repository_mock:

        repository_mock.return_value.prediction_stats.return_value = stats

        service = PredictionStatService()

        result = service.prediction_stats()

    repository_mock.return_value.prediction_stats.assert_called_once()

    assert result is not None
    assert result[1] == 200


def test_prediction_stats_none_result(app_context):
    stats = None

    with patch(
        "services.PredictionStatService.PredictionRepository"
    ) as repository_mock:

        repository_mock.return_value.prediction_stats.return_value = stats

        service = PredictionStatService()

        result = service.prediction_stats()

    repository_mock.return_value.prediction_stats.assert_called_once()

    assert result is not None
    assert result[1] == 200
