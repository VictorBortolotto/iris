
from unittest.mock import Mock, patch

from services.FindAllPredictionService import FindAllPredictionService
from mocks.dto_mocks import mock_consult_prediction


def test_find_all_prediction_success(app_context):
    repository = Mock()

    predictions = [
        mock_consult_prediction(),
        mock_consult_prediction(),
        mock_consult_prediction()
    ]

    repository.find_all_prediction.return_value = predictions

    service = FindAllPredictionService(repository)

    with patch("services.FindAllPredictionService.Pagination") as pagination_mock:
        pagination_mock.return_value.pagination.return_value = predictions

        result = service.find_all_prediction(None)

    repository.find_all_prediction.assert_called_once_with(None)
    pagination_mock.assert_called_once_with(predictions)
    pagination_mock.return_value.pagination.assert_called_once()

    assert result is not None


def test_find_all_prediction_with_specie_filter(app_context):
    repository = Mock()

    predictions = [mock_consult_prediction()]
    repository.find_all_prediction.return_value = predictions

    service = FindAllPredictionService(repository)

    with patch("services.FindAllPredictionService.Pagination") as pagination_mock:
        pagination_mock.return_value.pagination.return_value = predictions

        result = service.find_all_prediction("setosa")

    repository.find_all_prediction.assert_called_once_with("setosa")
    pagination_mock.assert_called_once_with(predictions)

    assert result is not None


def test_find_all_prediction_empty_result(app_context):
    repository = Mock()
    repository.find_all_prediction.return_value = []

    service = FindAllPredictionService(repository)

    result = service.find_all_prediction(None)

    repository.find_all_prediction.assert_called_once_with(None)

    assert result is not None


def test_find_all_prediction_none_result(app_context):
    repository = Mock()
    repository.find_all_prediction.return_value = None

    service = FindAllPredictionService(repository)

    result = service.find_all_prediction(None)

    repository.find_all_prediction.assert_called_once_with(None)

    assert result is not None


def test_find_all_prediction_empty_specie(app_context):
    repository = Mock()
    repository.find_all_prediction.return_value = []

    service = FindAllPredictionService(repository)

    result = service.find_all_prediction("")

    repository.find_all_prediction.assert_called_once_with(None)

    assert result is not None
