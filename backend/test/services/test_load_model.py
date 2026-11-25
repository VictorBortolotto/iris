
from unittest.mock import patch, Mock

import pytest

from services.LoadModel import LoadModel


def test_load_model_success():
    model = Mock()

    with patch("services.LoadModel.Path.exists", return_value=True):
        with patch("services.LoadModel.joblib.load", return_value=model) as joblib_mock:

            service = LoadModel()
            result = service.load_model()

    joblib_mock.assert_called_once_with(service.MODEL_PATH)

    assert result is not None
    assert result == model


def test_load_model_file_not_found():
    with patch("services.LoadModel.Path.exists", return_value=False):

        service = LoadModel()

        with pytest.raises(FileNotFoundError) as exception:
            service.load_model()

    assert "Modelo não encontrado" in str(exception.value)


def test_load_model_joblib_error():
    with patch("services.LoadModel.Path.exists", return_value=True):
        with patch(
            "services.LoadModel.joblib.load",
            side_effect=Exception("Erro ao carregar modelo")
        ):

            service = LoadModel()

            with pytest.raises(Exception) as exception:
                service.load_model()

    assert str(exception.value) == "Erro ao carregar modelo"
