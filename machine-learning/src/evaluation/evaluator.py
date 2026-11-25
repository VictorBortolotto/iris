
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
  accuracy_score,
  precision_score,
  recall_score,
  f1_score,
  confusion_matrix,
  classification_report
)


def evaluate_models(models, X_test, y_test, iris):

  results = []

  for name, model in models.items():

    predictions = model.predict(X_test)

    results.append({
      "model": name,
      "accuracy": accuracy_score(
        y_test, predictions
      ),
      "precision": precision_score(
        y_test, predictions, average="macro"
      ),
      "recall": recall_score(
        y_test, predictions, average="macro"
      ),
      "f1_score": f1_score(
        y_test, predictions, average="macro"
      )
    })

    print(f"\nRelatório: {name}")

    print(classification_report(
      y_test,
      predictions,
      target_names=iris.target_names
    ))

    cm = confusion_matrix(
      y_test,
      predictions,
      labels=[0, 1, 2]
    )

    sns.heatmap(
      cm,
      annot=True,
      fmt="d",
      xticklabels=iris.target_names,
      yticklabels=iris.target_names
    )

    plt.title(f"Matriz de Confusão - {name}")
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.savefig(
      f"reports/figures/{name.lower().replace(' ', '_')}.png"
    )
    plt.close()

  return pd.DataFrame(results)
