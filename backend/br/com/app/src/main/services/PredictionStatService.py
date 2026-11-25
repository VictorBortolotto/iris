from domain.repository.PredictionRepository import PredictionRepository
from utils.ApiResponse import ApiResponse

class PredictionStatService():
  def __init__(self):
    self.repository = PredictionRepository()

  def prediction_stats(self):
    stats = self.repository.prediction_stats()

    return ApiResponse.ok("Prediction stats retrived with success.", stats)