import shutil
from pathlib import Path

# Raiz do projeto unificado
ROOT_DIR = Path(__file__).resolve().parents[2]

SOURCE_MODEL = (
    ROOT_DIR / "classifier" / "artifacts" / "modelo_iris.pkl"
)

DESTINATION_DIR = ROOT_DIR / "backend" / "artifacts"
DESTINATION_MODEL = DESTINATION_DIR / "modelo_iris.pkl"


def deploy_model():
    if not SOURCE_MODEL.exists():
      raise FileNotFoundError(
        f"Modelo não encontrado: {SOURCE_MODEL}"
      )

    DESTINATION_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy2(SOURCE_MODEL, DESTINATION_MODEL)

    print("Modelo copiado para o backend com sucesso!")


if __name__ == "__main__":
    deploy_model()