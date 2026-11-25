
from unittest.mock import Mock, patch

from services.FindPredictionByIdService import FindPredictionByIdService
from mocks.dto_mocks import mock_consult_prediction


def test_find_prediction_by_id_success(app_context):
    prediction = mock_consult_prediction()

    with patch(
        "services.FindPredictionByIdService.PredictionRepository"
    ) as repository_mock:

        repository_mock.return_value.find_prediction_by_id.return_value = prediction

        service = FindPredictionByIdService()

        result = service.find_prediction_by_id(1)

    repository_mock.return_value.find_prediction_by_id.assert_called_once_with(1)

    assert result is not None
    assert result[1] == 200


def test_find_prediction_by_id_not_found(app_context):
    with patch(
        "services.FindPredictionByIdService.PredictionRepository"
    ) as repository_mock:

        repository_mock.return_value.find_prediction_by_id.return_value = None

        service = FindPredictionByIdService()

        result = service.find_prediction_by_id(999)

    repository_mock.return_value.find_prediction_by_id.assert_called_once_with(999)

    assert result is not None
    assert result[1] == 404
