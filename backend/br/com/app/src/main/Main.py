from flask import Flask
from flask_cors import CORS
from controller.PredictionController import PredictionController
from utils.CreateFolderDatabase import CreateFolderDatabase
from database.Database import Database
app = Flask(__name__)

CORS(app, resources={
    r"/prediction*": {
        "origins": ["null", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

def create_database_folder():
  CreateFolderDatabase.create_folder()

def initialize_database():
  Database().create_table()

def main():
  PredictionController(app)

def initialize_application():
  create_database_folder()
  initialize_database()
  main()


initialize_application()

if __name__ == "__main__":
  app.run(port=8080)