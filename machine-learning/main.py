from src.data.loader import (
    load_dataset,
    validate_dataset,
    split_dataset
)

from src.models.model_factory import create_models
from src.models.hyperparameters import get_hyperparameters

from src.training.trainer import train_models

from src.evaluation.evaluator import evaluate_models

from src.export.model_exporter import export_model


def main():

  # HU01 - Preparação
  X, y, iris = load_dataset()

  validate_dataset(X, y)

  X_train, X_test, y_train, y_test = split_dataset(X, y)

  # HU02 - Treinamento
  models = create_models()
  params = get_hyperparameters()

  best_models, cv_results = train_models(
    models,
    params,
    X_train,
    y_train
  )

  # HU03 - Avaliação
  results = evaluate_models(
    best_models,
    X_test,
    y_test,
    iris
  )

  print("\nResultados:")
  print(results)

  results.to_csv(
    "reports/results/resultados_modelos.csv",
    index=False
  )

  # Selecionar o melhor modelo pela validação cruzada
  best_name = max(
    cv_results,
    key=lambda name: cv_results[name]["accuracy"]
  )

  best_model = best_models[best_name]

  # Exportar modelo
  export_model(
    best_model,
    "artifacts/modelo_iris.pkl"
  )

  print(f"\nMelhor modelo: {best_name}")

if __name__ == "__main__":
  main()