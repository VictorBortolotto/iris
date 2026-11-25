import joblib
from pathlib import Path

class LoadModel:
  def load_model(self):
    base_path = Path(__file__).resolve().parents[6]

    model_path = base_path / "artifacts" / "modelo_iris.pkl"

    model = joblib.load(model_path)

    return model