import pandas as pd
import datetime
from domain.repository.PredictionRepository import PredictionRepository

class PredictionService:
  def __init__(self):
    self.predition_repository = PredictionRepository()
    self.FEATURE_NAMES = [
      "sepal length (cm)",
      "sepal width (cm)",
      "petal length (cm)",
      "petal width (cm)"
    ]

    self.SPECIES = [
      "Iris Setosa",
      "Iris Versicolor",
      "Iris Virginica"
    ]

  def predict_species(self, model, request):
    features = [
      request["sepal_length"],
      request["sepal_width"],
      request["petal_length"],
      request["petal_width"]
    ]

    id_request = self.predition_repository.insert_request_data(request)

    data = pd.DataFrame(
      [features],
      columns=self.FEATURE_NAMES
    )

    prediction = model.predict(data)[0]
    probabilities = model.predict_proba(data)[0]

    self.predition_repository.insert_query_data(self.SPECIES[int(prediction)], model.predict_proba(data)[0][0], model.predict_proba(data)[0][1], model.predict_proba(data)[0][2], datetime.datetime.now(), id_request)

    return {
      "species": self.SPECIES[int(prediction)],
      "probabilities": {
        self.SPECIES[int(class_id)]: float(probability)
        for class_id, probability
        in zip(model.classes_, probabilities)
      }
    }