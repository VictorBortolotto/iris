from domain.repository.PredictionRepository import PredictionRepository
from utils.ApiResponse import ApiResponse
from utils.Pagination import Pagination

class FindAllPredictionService():
  def __init__(self, repository=None):
    self.repository = repository or PredictionRepository()

  def find_all_prediction(self, nm_specie):
    if nm_specie == '' or nm_specie is None:
      nm_specie = None

    predictions = self.repository.find_all_prediction(nm_specie)

    if predictions is None or predictions == []:
      return ApiResponse.not_found("Predictions not found.")

    predictions = Pagination(predictions).pagination()

    return ApiResponse.ok("Predictions retrived with success.", predictions)

