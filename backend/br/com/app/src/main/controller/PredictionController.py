from flask import request
from utils.LoadModel import LoadModel
from services.PredictionService import PredictionService
from services.FindAllPredictionService import FindAllPredictionService
from services.FindPredictionByIdService import FindPredictionByIdService
from services.PredictionStatService import PredictionStatService

class PredictionController:
  def __init__(self, app):
    self.app = app
    self.model = LoadModel().load_model()
    self.prediction_service = PredictionService()
    self.find_all_prediction_service = FindAllPredictionService()
    self.find_prediction_by_id_service = FindPredictionByIdService()
    self.prediction_stats_service = PredictionStatService()
    self.default_route = "/prediction"
    self.register_routes()

  def register_routes(self):

    @self.app.route(self.default_route + "/predict", methods=['POST'])
    def classify_route():
      json = request.get_json()
      return self.prediction_service.predict_species(self.model, json)

    @self.app.route(self.default_route + "/all", methods=['GET'])
    def find_all_prediction():
      specie = request.args.get("specie")
      return self.find_all_prediction_service.find_all_prediction(specie)

    @self.app.route(self.default_route + "/<id>", methods=['GET'])
    def find_prediction_by_id(id):
      return self.find_prediction_by_id_service.find_prediction_by_id(id)
    
    @self.app.route(self.default_route + "/stats", methods=['GET'])
    def prediction_stats():
      return self.prediction_stats_service.prediction_stats()
      