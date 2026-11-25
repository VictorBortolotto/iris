
import pytest
from unittest.mock import patch

from domain.repository.PredictionRepository import PredictionRepository


@pytest.fixture
def repository():
  with patch("domain.repository.PredictionRepository.Database") as database_mock:
    repo = PredictionRepository()
    yield repo, database_mock.return_value


# --------------------------------------------------
# insert_request_data
# --------------------------------------------------

def test_insert_request_data(repository):
  repo, database = repository

  request = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }

  database.insert.return_value = 10

  result = repo.insert_request_data(request)

  assert result == 10

  database.insert.assert_called_once()

  sql, params = database.insert.call_args.args

  assert "INSERT INTO REQUEST_DATA" in sql.upper()
  assert params == (5.1, 3.5, 1.4, 0.2)


def test_insert_request_data_database_returns_none(repository):
  repo, database = repository

  request = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }

  database.insert.return_value = None

  result = repo.insert_request_data(request)

  assert result is None


# --------------------------------------------------
# insert_query_data
# --------------------------------------------------

def test_insert_query_data(repository):
  repo, database = repository

  database.insert.return_value = 20

  result = repo.insert_query_data(
    "Iris Setosa",
    0.95,
    0.03,
    0.02,
    "2026-11-25 10:00:00",
    10
  )

  assert result == 20

  database.insert.assert_called_once()

  sql, params = database.insert.call_args.args

  assert "INSERT INTO QUERY_DATA" in sql.upper()
  assert params == (
    "Iris Setosa",
    0.95,
    0.03,
    0.02,
    "2026-11-25 10:00:00",
    10
  )


def test_insert_query_data_database_returns_none(repository):
  repo, database = repository

  database.insert.return_value = None

  result = repo.insert_query_data(
    "Iris Versicolor",
    0.10,
    0.80,
    0.10,
    "2026-11-25 10:00:00",
    15
  )

  assert result is None


# --------------------------------------------------
# find_all_prediction
# --------------------------------------------------

def test_find_all_prediction_success(repository):
  repo, database = repository

  results = [
    (1, 5.1, 3.5, 1.4, 0.2, "Iris Setosa",
      0.95, 0.03, 0.02, "2026-11-25 10:00:00"),

    (2, 6.0, 2.9, 4.5, 1.5, "Iris Versicolor",
      0.05, 0.90, 0.05, "2026-11-25 11:00:00")
  ]

  database.find_all_by.return_value = results

  with patch(
    "domain.repository.PredictionRepository.ConsultPredictionDto"
  ) as dto_mock:

    result = repo.find_all_prediction(None)

    assert len(result) == 2
    assert result == [dto_mock.return_value, dto_mock.return_value]

    assert dto_mock.call_count == 2

    dto_mock.assert_any_call(
      1, 5.1, 3.5, 1.4, 0.2, "Iris Setosa",
      0.95, 0.03, 0.02, "2026-11-25 10:00:00"
    )

    dto_mock.assert_any_call(
      2, 6.0, 2.9, 4.5, 1.5, "Iris Versicolor",
      0.05, 0.90, 0.05, "2026-11-25 11:00:00"
    )

  database.find_all_by.assert_called_once()

  sql, params = database.find_all_by.call_args.args

  assert "SELECT" in sql.upper()
  assert "QUERY_DATA" in sql.upper()
  assert params == (None, None)


def test_find_all_prediction_with_specie_filter(repository):
  repo, database = repository

  database.find_all_by.return_value = []

  result = repo.find_all_prediction("Iris Setosa")

  assert result == []

  _, params = database.find_all_by.call_args.args

  assert params == ("Iris Setosa", "Iris Setosa")


def test_find_all_prediction_returns_none(repository):
  repo, database = repository

  database.find_all_by.return_value = None

  result = repo.find_all_prediction(None)

  assert result is None


def test_find_all_prediction_empty_list(repository):
  repo, database = repository

  database.find_all_by.return_value = []

  result = repo.find_all_prediction(None)

  assert result == []


# --------------------------------------------------
# find_prediction_by_id
# --------------------------------------------------

def test_find_prediction_by_id_success(repository):
  repo, database = repository

  database.find_by_id.return_value = (
    1, 5.1, 3.5, 1.4, 0.2, "Iris Setosa",
    0.95, 0.03, 0.02, "2026-11-25 10:00:00"
  )

  with patch(
    "domain.repository.PredictionRepository.ConsultPredictionDto"
  ) as dto_mock:

    result = repo.find_prediction_by_id(1)

    assert result == dto_mock.return_value

    dto_mock.assert_called_once_with(
      1, 5.1, 3.5, 1.4, 0.2, "Iris Setosa",
      0.95, 0.03, 0.02, "2026-11-25 10:00:00"
    )

  database.find_by_id.assert_called_once()

  sql, params = database.find_by_id.call_args.args

  assert "SELECT" in sql.upper()
  assert params == (1,)


def test_find_prediction_by_id_not_found(repository):
  repo, database = repository

  database.find_by_id.return_value = None

  with patch(
      "domain.repository.PredictionRepository.ConsultPredictionDto"
  ) as dto_mock:

    result = repo.find_prediction_by_id(999)

    assert result is None
    dto_mock.assert_not_called()


# --------------------------------------------------
# prediction_stats
# --------------------------------------------------

def test_prediction_stats_success(repository):
  repo, database = repository

  database.find_by_id.return_value = (
    100,
    30,
    30.0,
    40,
    40.0,
    30,
    30.0
  )

  with patch(
    "domain.repository.PredictionRepository.PredictionStatsDto"
  ) as dto_mock:

    result = repo.prediction_stats()

    assert result == dto_mock.return_value

    dto_mock.assert_called_once_with(
      100,
      30,
      30.0,
      40,
      40.0,
      30,
      30.0
    )

  database.find_by_id.assert_called_once()

  sql, params = database.find_by_id.call_args.args

  assert "COUNT(*)" in sql.upper()
  assert "SUM(CASE" in sql.upper()
  assert "QUERY_DATA" in sql.upper()
  assert params == ()


def test_prediction_stats_returns_none(repository):
  repo, database = repository

  database.find_by_id.return_value = None

  with patch(
    "domain.repository.PredictionRepository.PredictionStatsDto"
  ) as dto_mock:

    result = repo.prediction_stats()

    assert result is None
    dto_mock.assert_not_called()
