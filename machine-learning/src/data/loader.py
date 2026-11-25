
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def load_dataset():
  iris = load_iris()

  X = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
  )

  y = pd.Series(iris.target, name="species")

  return X, y, iris


def validate_dataset(X, y):
  if X.empty or y.empty:
    raise ValueError("Dataset vazio.")

  if X.isnull().values.any():
    raise ValueError("Existem valores ausentes.")

  if not X.map(lambda value: pd.notna(value)).all().all():
    raise ValueError("Existem valores inconsistentes.")

  if not (X.dtypes.apply(
    lambda dtype: pd.api.types.is_numeric_dtype(dtype)
  )).all():
    raise ValueError("Atributos devem ser numéricos.")

  if not set(y.unique()).issubset({0, 1, 2}):
    raise ValueError("Espécies inválidas.")


def split_dataset(X, y):
  return train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
  )
