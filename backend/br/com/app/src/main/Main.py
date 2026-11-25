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

##swagger = SwaggerConfig().config(app)

def create_database_folder():
  CreateFolderDatabase.create_folder()

def initialize_database():
  Database().create_table()

def main():
  PredictionController(app)

create_database_folder()
initialize_database()
main()

if __name__ == "__main__":
  app.run(port=8080)