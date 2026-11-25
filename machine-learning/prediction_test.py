import joblib
from src.prediction.predictor import predict_species

# Carrega o modelo treinado
modelo = joblib.load("artifacts/modelo_iris.pkl")

# Exemplo de medidas de uma flor
caracteristicas = [10.1, 3.5, 1.4, 0.2]

# Realiza a classificação
resultado = predict_species(modelo, caracteristicas)

print("Espécie prevista:", resultado["species"])
print("\nProbabilidades:")

for especie, probabilidade in resultado["probabilities"].items():
  print(f"{especie}: {probabilidade:.2%}")