from domain.repository.PredictionRepository import PredictionRepository
from utils.ApiResponse import ApiResponse

class FindPredictionByIdService():
  def __init__(self):
    self.repository = PredictionRepository()

  def find_prediction_by_id(self, id):
    prediction = self.repository.find_prediction_by_id(id)

    if prediction is None:
      return ApiResponse.not_found("Prediction not found.")

    return ApiResponse.ok("Prediction retrived with success.", prediction)