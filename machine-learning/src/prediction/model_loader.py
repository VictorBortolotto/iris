
import joblib


def load_trained_model(model_path):
  return joblib.load(model_path)
