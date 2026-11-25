
import sqlite3
import pytest

from unittest.mock import MagicMock, patch, mock_open

from database.Database import Database


@pytest.fixture
def database():
  db = Database()

  conn = MagicMock()
  cursor = MagicMock()

  conn.cursor.return_value = cursor
  cursor.execute.return_value = cursor

  return db, conn, cursor


# --------------------------------------------------
# get_connection
# --------------------------------------------------

def test_get_connection_success():
  db = Database()

  with patch("database.Database.sqlite3.connect") as connect_mock:
    result = db.get_connection()

    connect_mock.assert_called_once()

    assert result == connect_mock.return_value

    db_path = connect_mock.call_args.args[0]

    assert db_path.endswith("database.db")


# --------------------------------------------------
# create_table
# --------------------------------------------------

def test_create_table_success(database):
  db, conn, cursor = database

  sql_script = """
    CREATE TABLE IF NOT EXISTS test (
      id INTEGER PRIMARY KEY
    );
  """

  with patch.object(db, "get_connection", return_value=conn):
    with patch(
      "pathlib.Path.open",
      mock_open(read_data=sql_script)
    ):
      db.create_table()

  cursor.executescript.assert_called_once_with(sql_script)
  conn.commit.assert_called_once()
  conn.close.assert_called_once()


# --------------------------------------------------
# insert
# --------------------------------------------------

def test_insert_success(database):
  db, conn, cursor = database

  cursor.lastrowid = 10

  query = "INSERT INTO test (name) VALUES (?)"
  params = ("Iris Setosa",)

  with patch.object(db, "get_connection", return_value=conn):
    result = db.insert(query, params)

  assert result == 10

  cursor.execute.assert_called_once_with(query, params)
  conn.commit.assert_called_once()
  conn.close.assert_called_once()


def test_insert_database_error(database):
  db, conn, cursor = database

  cursor.execute.side_effect = sqlite3.Error("Database error")

  with patch.object(db, "get_connection", return_value=conn):
    with pytest.raises(sqlite3.Error):
      db.insert("INSERT INTO test VALUES (?)", (1,))

  conn.rollback.assert_called_once()
  conn.close.assert_called_once()


# --------------------------------------------------
# delete_by_id
# --------------------------------------------------

def test_delete_by_id_success(database):
  db, conn, cursor = database

  cursor.rowcount = 1

  query = "DELETE FROM test WHERE id = ?"
  params = (10,)

  with patch.object(db, "get_connection", return_value=conn):
    result = db.delete_by_id(query, params)

  assert result == 1

  cursor.execute.assert_called_once_with(query, params)
  conn.commit.assert_called_once()
  conn.close.assert_called_once()


def test_delete_by_id_database_error(database):
  db, conn, cursor = database

  cursor.execute.side_effect = sqlite3.Error("Database error")

  with patch.object(db, "get_connection", return_value=conn):
    with pytest.raises(sqlite3.Error):
      db.delete_by_id("DELETE FROM test WHERE id = ?", (10,))

  conn.rollback.assert_called_once()
  conn.close.assert_called_once()


# --------------------------------------------------
# find_by_id
# --------------------------------------------------

def test_find_by_id_success(database):
  db, conn, cursor = database

  expected_result = (1, "Iris Setosa")
  cursor.fetchone.return_value = expected_result

  query = "SELECT * FROM test WHERE id = ?"
  params = (1,)

  with patch.object(db, "get_connection", return_value=conn):
    result = db.find_by_id(query, params)

  assert result == expected_result

  cursor.execute.assert_called_once_with(query, params)
  cursor.fetchone.assert_called_once()
  conn.close.assert_called_once()


def test_find_by_id_not_found(database):
  db, conn, cursor = database

  cursor.fetchone.return_value = None

  with patch.object(db, "get_connection", return_value=conn):
    result = db.find_by_id(
      "SELECT * FROM test WHERE id = ?",
      (999,)
    )

  assert result is None
  conn.close.assert_called_once()


def test_find_by_id_database_error(database):
  db, conn, cursor = database

  cursor.execute.side_effect = sqlite3.Error("Database error")

  with patch.object(db, "get_connection", return_value=conn):
    with pytest.raises(sqlite3.Error):
      db.find_by_id("SELECT * FROM test WHERE id = ?", (1,))

  conn.rollback.assert_called_once()
  conn.close.assert_called_once()


# --------------------------------------------------
# find_all_by
# --------------------------------------------------

def test_find_all_by_success(database):
  db, conn, cursor = database

  expected_result = [
    (1, "Iris Setosa"),
    (2, "Iris Versicolor")
  ]

  cursor.fetchall.return_value = expected_result

  query = "SELECT * FROM test WHERE specie = ?"
  params = ("Iris Setosa",)

  with patch.object(db, "get_connection", return_value=conn):
    result = db.find_all_by(query, params)

  assert result == expected_result

  cursor.execute.assert_called_once_with(query, params)
  cursor.fetchall.assert_called_once()
  conn.close.assert_called_once()


def test_find_all_by_empty_list(database):
  db, conn, cursor = database

  cursor.fetchall.return_value = []

  with patch.object(db, "get_connection", return_value=conn):
    result = db.find_all_by("SELECT * FROM test", ())

  assert result == []
  conn.close.assert_called_once()


def test_find_all_by_database_error(database):
  db, conn, cursor = database

  cursor.execute.side_effect = sqlite3.Error("Database error")

  with patch.object(db, "get_connection", return_value=conn):
    with pytest.raises(sqlite3.Error):
      db.find_all_by("SELECT * FROM test", ())

  conn.rollback.assert_called_once()
  conn.close.assert_called_once()


# --------------------------------------------------
# update_by_id
# --------------------------------------------------

def test_update_by_id_success(database):
  db, conn, cursor = database

  cursor.rowcount = 1

  query = "UPDATE test SET name = ? WHERE id = ?"
  params = ("Iris Virginica", 1)

  with patch.object(db, "get_connection", return_value=conn):
    result = db.update_by_id(query, params)

  assert result == 1

  cursor.execute.assert_called_once_with(query, params)
  conn.commit.assert_called_once()
  conn.close.assert_called_once()


def test_update_by_id_database_error(database):
  db, conn, cursor = database

  cursor.execute.side_effect = sqlite3.Error("Database error")

  with patch.object(db, "get_connection", return_value=conn):
    with pytest.raises(sqlite3.Error):
      db.update_by_id(
        "UPDATE test SET name = ? WHERE id = ?",
        ("Iris Setosa", 1)
      )

  conn.rollback.assert_called_once()
  conn.close.assert_called_once()
