import joblib
from pathlib import Path

class LoadModel:

  def __init__(self):
    BASE_DIR = Path(__file__).resolve().parents[4]
    self.MODEL_PATH = BASE_DIR / "artifacts" / "modelo_iris.pkl"

  def load_model(self):
    if not self.MODEL_PATH.exists():
      raise FileNotFoundError(
        f"Modelo não encontrado: {self.MODEL_PATH}"
      )

    return joblib.load(self.MODEL_PATH)