
import joblib
import os

def export_model(model, path):
  os.makedirs(
    os.path.dirname(path) or ".",
    exist_ok=True
  )

  joblib.dump(model, path)

  print(f"Modelo exportado em: {path}")
