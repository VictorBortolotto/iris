# Iris Classifier

Projeto de Machine Learning para classificação supervisionada de flores do gênero **Iris**, utilizando o Iris Dataset. O módulo prepara os dados, treina e compara diferentes algoritmos de classificação, avalia seus resultados e exporta o melhor modelo treinado para utilização posterior.

O projeto faz parte de uma aplicação maior que prevê a integração de um módulo de Machine Learning com um Backend e uma interface web. Este repositório/pasta documenta especificamente o componente `classifier`.

---

## Objetivos

### Objetivo geral

Desenvolver e avaliar um modelo de Machine Learning capaz de identificar as espécies de flores do gênero Iris a partir de quatro características morfológicas: comprimento e largura das sépalas e comprimento e largura das pétalas.

### Objetivos específicos

- Utilizar o Iris Dataset como conjunto de dados para classificação supervisionada.
- Carregar e validar os dados, verificando valores ausentes, inconsistências e tipos dos atributos.
- Separar os dados em conjuntos de treinamento e teste.
- Treinar e comparar diferentes algoritmos de classificação.
- Otimizar os hiperparâmetros dos modelos por meio de validação cruzada.
- Avaliar o desempenho dos modelos utilizando métricas de classificação.
- Gerar relatórios e matrizes de confusão para apoiar a análise dos resultados.
- Selecionar o melhor modelo e exportá-lo em formato `.pkl`.
- Disponibilizar funções para carregar o modelo exportado e realizar previsões com novos dados.

## Dataset

O projeto utiliza o **Iris Dataset**, disponibilizado pelo módulo `sklearn.datasets` do Scikit-learn. Portanto, não é necessário baixar ou fornecer um arquivo CSV manualmente.

O conjunto contém 150 registros, distribuídos entre três espécies:

- Iris Setosa
- Iris Versicolor
- Iris Virginica

Cada registro possui quatro atributos, medidos em centímetros:

| Atributo | Descrição |
|---|---|
| `sepal length (cm)` | Comprimento da sépala |
| `sepal width (cm)` | Largura da sépala |
| `petal length (cm)` | Comprimento da pétala |
| `petal width (cm)` | Largura da pétala |

O objetivo do classificador é utilizar essas quatro medidas para prever a espécie correspondente.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação do projeto |
| Pandas | Organização e manipulação dos dados |
| NumPy | Operações numéricas |
| Scikit-learn | Dataset, pré-processamento, algoritmos, validação cruzada e métricas |
| Matplotlib | Geração de gráficos |
| Seaborn | Visualização das matrizes de confusão |
| Joblib | Serialização e carregamento do modelo `.pkl` |

## Algoritmos de classificação

O projeto compara quatro algoritmos:

- **K-Nearest Neighbors (KNN):** classifica uma amostra considerando os exemplos mais próximos.
- **Decision Tree:** utiliza regras organizadas em uma estrutura de árvore para realizar a classificação.
- **Naive Bayes:** aplica o teorema de Bayes com a hipótese de independência condicional entre os atributos.
- **Support Vector Machine (SVM):** busca uma fronteira de decisão que separe as classes.

Os hiperparâmetros são testados com `GridSearchCV`. A avaliação durante a busca utiliza validação cruzada estratificada com cinco partições (`StratifiedKFold`).

Para KNN e SVM, o pipeline inclui normalização dos atributos. O projeto testa `StandardScaler` e `MinMaxScaler` na busca de hiperparâmetros. Decision Tree e Naive Bayes são executados sem etapa de normalização.

## Estrutura do projeto

```text
classifier/
├── artifacts/
│   └── modelo_iris.pkl
├── reports/
│   ├── figures/
│   │   ├── decision_tree.png
│   │   ├── knn.png
│   │   ├── naive_bayes.png
│   │   └── svm.png
│   └── results/
│       └── resultados_modelos.csv
├── scripts/
│   └── deploy_model.py
├── src/
│   ├── data/
│   │   └── loader.py
│   ├── evaluation/
│   │   └── evaluator.py
│   ├── export/
│   │   └── model_exporter.py
│   ├── models/
│   │   ├── hyperparameters.py
│   │   └── model_factory.py
│   ├── prediction/
│   │   ├── model_loader.py
│   │   └── predictor.py
│   ├── preprocessing/
│   │   └── transformer.py
│   └── training/
│       └── trainer.py
├── main.py
├── prediction_test.py
├── requirements.txt
└── README.md
```

### Responsabilidade dos principais módulos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Orquestra o fluxo de preparação, treinamento, avaliação e exportação |
| `src/data/loader.py` | Carrega, valida e divide o dataset |
| `src/models/model_factory.py` | Cria os pipelines dos algoritmos |
| `src/models/hyperparameters.py` | Define os hiperparâmetros testados |
| `src/training/trainer.py` | Executa o treinamento e a busca de hiperparâmetros |
| `src/evaluation/evaluator.py` | Calcula métricas, apresenta relatórios e gera matrizes de confusão |
| `src/export/model_exporter.py` | Exporta o modelo treinado utilizando Joblib |
| `src/prediction/model_loader.py` | Carrega um modelo previamente exportado |
| `src/prediction/predictor.py` | Valida as características recebidas e realiza a previsão |
| `scripts/deploy_model.py` | Copia o modelo exportado para a pasta de artefatos do backend, na estrutura de projeto unificada |
| `prediction_test.py` | Demonstra o carregamento do modelo e a realização de uma classificação |

## Como executar o projeto

### 1. Pré-requisitos

- Python instalado (recomenda-se Python 3.10 ou superior).
- Git, caso queira clonar o repositório.

### 2. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd classifier
```

Substitua `<URL_DO_REPOSITORIO>` pelo endereço do repositório Git.

Se você já possui o projeto localmente, basta abrir um terminal na pasta `classifier`.

### 3. Criar um ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as bibliotecas necessárias:

```text
pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
```

### 5. Executar o treinamento

Na raiz da pasta `classifier`, execute:

```bash
python main.py
```

O programa executará as seguintes etapas:

1. Carregamento do Iris Dataset.
2. Validação dos dados.
3. Separação em conjuntos de treinamento e teste.
4. Criação dos pipelines dos algoritmos.
5. Busca dos melhores hiperparâmetros por validação cruzada.
6. Avaliação dos modelos com os dados de teste.
7. Geração das matrizes de confusão e dos resultados.
8. Seleção do melhor modelo com base na acurácia média da validação cruzada.
9. Exportação do modelo selecionado.

A execução pode levar algum tempo devido à busca de hiperparâmetros realizada para cada algoritmo.

## Arquivos gerados

Após executar `python main.py`, os seguintes arquivos serão criados ou atualizados:

| Caminho | Conteúdo |
|---|---|
| `artifacts/modelo_iris.pkl` | Modelo selecionado e treinado |
| `reports/results/resultados_modelos.csv` | Métricas de avaliação dos modelos |
| `reports/figures/knn.png` | Matriz de confusão do KNN |
| `reports/figures/decision_tree.png` | Matriz de confusão da árvore de decisão |
| `reports/figures/naive_bayes.png` | Matriz de confusão do Naive Bayes |
| `reports/figures/svm.png` | Matriz de confusão do SVM |

O diretório `artifacts` é criado automaticamente durante a exportação, assim como o diretório informado ao exportador.

### Como o melhor modelo é selecionado?

A seleção utiliza a maior acurácia média obtida durante a validação cruzada (`cv_results`), conforme implementado no `main.py`.

As métricas calculadas na etapa de avaliação com o conjunto de teste são:

- **Accuracy (acurácia):** proporção de previsões corretas.
- **Precision (precisão):** proporção de previsões positivas corretas, considerando a média macro entre as classes.
- **Recall (revocação):** proporção de exemplos de cada classe identificados corretamente, considerando a média macro.
- **F1-score:** média harmônica entre precisão e recall, considerando a média macro.

A matriz de confusão permite observar a quantidade de previsões corretas e incorretas para cada espécie.

## Como carregar e utilizar o arquivo `.pkl`

O arquivo `artifacts/modelo_iris.pkl` contém o melhor pipeline treinado. Como o pipeline é exportado por completo, ele preserva também a etapa de normalização, quando aplicável.

Para carregar o modelo:

```python
import joblib

model = joblib.load("artifacts/modelo_iris.pkl")
```

O projeto também disponibiliza a função `load_trained_model`:

```python
from src.prediction.model_loader import load_trained_model

model = load_trained_model("artifacts/modelo_iris.pkl")
```

### Realizar uma previsão

Utilize a função `predict_species`:

```python
from src.prediction.predictor import predict_species
from src.prediction.model_loader import load_trained_model

model = load_trained_model("artifacts/modelo_iris.pkl")

features = [5.1, 3.5, 1.4, 0.2]

result = predict_species(model, features)

print("Espécie prevista:", result["species"])
print("Probabilidades:", result["probabilities"])
```

A lista de características deve respeitar esta ordem:

1. Comprimento da sépala (`sepal length (cm)`).
2. Largura da sépala (`sepal width (cm)`).
3. Comprimento da pétala (`petal length (cm)`).
4. Largura da pétala (`petal width (cm)`).

A função valida se foram fornecidas exatamente quatro características numéricas e se os valores são maiores que zero. O retorno contém a espécie prevista e as probabilidades estimadas para as três classes.

### Executar o teste de predição

Também é possível executar o script de demonstração:

```bash
python prediction_test.py
```

Esse script carrega `artifacts/modelo_iris.pkl` e realiza uma classificação de exemplo. Execute-o somente depois de gerar o arquivo do modelo com `python main.py`.

## Integração com o Backend

O modelo exportado pode ser utilizado pelo Backend sem executar novamente o treinamento. A separação entre treinamento e inferência permite que o Backend carregue o artefato já treinado e utilize a função de predição para classificar novas flores.

Na estrutura unificada do projeto, o script `scripts/deploy_model.py` copia o arquivo:

```text
classifier/artifacts/modelo_iris.pkl
```

para:

```text
backend/artifacts/modelo_iris.pkl
```

Para executar esse script, a estrutura de diretórios deve conter `classifier` e `backend` como pastas irmãs, conforme esperado pelo caminho configurado no próprio script. A execução deve ser feita a partir da pasta `classifier`:

```bash
python scripts/deploy_model.py
```

O script de deploy apenas copia o artefato existente; ele não realiza o treinamento. Portanto, execute `python main.py` antes da cópia.

**Compatibilidade:** utilize versões compatíveis de Python e Scikit-learn no ambiente de treinamento e no Backend. Modelos serializados com Joblib podem não ser compatíveis entre versões diferentes das bibliotecas.

## Observações

- O treinamento e a avaliação são executados localmente a partir de `main.py`.
- O dataset é carregado diretamente pelo Scikit-learn.
- O arquivo `.pkl` é um artefato gerado pelo treinamento; caso não esteja presente, execute `python main.py`.
- As probabilidades retornadas são estimativas produzidas pelo classificador, não garantias de acerto.
- O notebook do Google Colab é uma alternativa para executar o fluxo de treinamento em outro ambiente. Este README descreve o projeto `classifier` e sua execução por meio dos scripts Python.

---

## Licença

Consulte o arquivo [`LICENSE`](LICENSE) para obter as informações de licenciamento do projeto.
