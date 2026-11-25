
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def get_hyperparameters():

  return {
    "KNN": {
      "scaler": [
        StandardScaler(),
        MinMaxScaler()
      ],
      "model__n_neighbors": [3, 5, 7, 9],
      "model__weights": ["uniform", "distance"],
      "model__p": [1, 2]
    },

    "Decision Tree": {
      "model__criterion": ["gini", "entropy"],
      "model__max_depth": [None, 2, 3, 4, 5],
      "model__min_samples_split": [2, 4]
    },

    "Naive Bayes": {
      "model__var_smoothing": [
        1e-9, 1e-8, 1e-7, 1e-6
      ]
    },

    "SVM": {
      "scaler": [
        StandardScaler(),
        MinMaxScaler()
      ],
      "model__C": [0.1, 1, 10, 100],
      "model__kernel": ["linear", "rbf"],
      "model__gamma": ["scale", "auto"]
    }
  }
