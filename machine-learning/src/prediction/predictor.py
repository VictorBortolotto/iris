
import pandas as pd


FEATURE_NAMES = [
  "sepal length (cm)",
  "sepal width (cm)",
  "petal length (cm)",
  "petal width (cm)"
]

SPECIES = [
  "Iris Setosa",
  "Iris Versicolor",
  "Iris Virginica"
]


def predict_species(model, features):

  if len(features) != 4:
    raise ValueError(
      "São necessárias exatamente quatro características."
    )

  if any(not isinstance(value, (int, float)) or not pd.notna(value) for value in features):
    raise ValueError(
      "As características devem ser valores numéricos válidos."
    )

  if any(value <= 0 for value in features):
    raise ValueError(
      "As características devem ser maiores que zero."
    )

  data = pd.DataFrame(
    [features],
    columns=FEATURE_NAMES
  )

  prediction = model.predict(data)[0]

  probabilities = model.predict_proba(data)[0]

  return {
    "species": SPECIES[int(prediction)],
    "probabilities": {
      SPECIES[int(class_id)]: float(probability)
      for class_id, probability in zip(
        model.classes_,
        probabilities
      )
    }
  }
