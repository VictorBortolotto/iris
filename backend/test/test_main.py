
from unittest.mock import patch

import Main


def test_create_database_folder():
  with patch(
    "Main.CreateFolderDatabase.create_folder"
  ) as create_folder_mock:

    Main.create_database_folder()

    create_folder_mock.assert_called_once()


def test_initialize_database():
  with patch(
    "Main.Database"
  ) as database_mock:

    Main.initialize_database()

    database_mock.assert_called_once_with()
    database_mock.return_value.create_table.assert_called_once()


def test_main():
  with patch(
    "Main.PredictionController"
  ) as controller_mock:

    Main.main()

    controller_mock.assert_called_once_with(Main.app)


def test_initialize_application():
  with patch(
    "Main.create_database_folder"
  ) as create_folder_mock, patch(
    "Main.initialize_database"
  ) as initialize_database_mock, patch(
    "Main.main"
  ) as main_mock:

    Main.initialize_application()

    create_folder_mock.assert_called_once()
    initialize_database_mock.assert_called_once()
    main_mock.assert_called_once()


def test_app_is_flask_instance():
  from flask import Flask

  assert isinstance(Main.app, Flask)


def test_cors_configuration():
  client = Main.app.test_client()

  response = client.options(
    "/prediction/predict",
    headers={
      "Origin": "http://localhost:3000",
      "Access-Control-Request-Method": "POST",
      "Access-Control-Request-Headers": "Content-Type"
    }
  )

  assert response.headers.get("Access-Control-Allow-Origin") == "http://localhost:3000"
  assert "POST" in response.headers.get("Access-Control-Allow-Methods", "")
