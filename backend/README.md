# Iris Classifier — Backend

API REST responsável por classificar flores do conjunto de dados **Iris** a partir das medidas das sépalas e pétalas. O backend carrega um modelo de Machine Learning serializado em `artifacts/modelo_iris.pkl`, realiza a predição, calcula as probabilidades por espécie e persiste as consultas para posterior consulta e geração de estatísticas.

## Funcionalidades

- Classificação de uma flor a partir de quatro medidas numéricas.
- Retorno da espécie prevista e das probabilidades para *Iris Setosa*, *Iris Versicolor* e *Iris Virginica*.
- Persistência dos dados de entrada, resultado e probabilidades em banco SQLite.
- Consulta de todas as classificações, com filtro opcional por espécie.
- Consulta de uma classificação pelo identificador.
- Consulta de estatísticas: total de classificações, quantidade e percentual por espécie.

## Tecnologias

- **Python** — linguagem da aplicação.
- **Flask** — criação da API HTTP.
- **Flask-CORS** — configuração de Cross-Origin Resource Sharing.
- **Pandas** — preparação dos atributos de entrada para o modelo.
- **Joblib** — carregamento do modelo serializado.
- **SQLite** — armazenamento local das requisições e classificações.
- **scikit-learn** — modelo de classificação disponibilizado no artefato `.pkl`.

> O repositório não contém um `requirements.txt` nem fixa versões das dependências. A lista acima foi identificada a partir dos imports e do uso do artefato; instale versões compatíveis entre si e com a versão de Python usada para treinar o modelo.

## Estrutura do projeto

```text
backend/
├── artifacts/
│   └── modelo_iris.pkl
├── br/com/app/src/
│   ├── main/
│   │   ├── controller/
│   │   │   └── PredictionController.py
│   │   ├── database/
│   │   │   └── Database.py
│   │   ├── domain/
│   │   │   ├── dto/
│   │   │   └── repository/
│   │   ├── services/
│   │   │   ├── FindAllPredictionService.py
│   │   │   ├── FindPredictionByIdService.py
│   │   │   ├── LoadModel.py
│   │   │   ├── PredictionService.py
│   │   │   └── PredictionStatService.py
│   │   ├── utils/
│   │   └── Main.py
│   └── resources/
│       └── create_tables.sql
├── database/                 # criado automaticamente na inicialização
├── test/                     # diretório presente; sem testes incluídos no ZIP
├── .gitignore
└── README.md
```

### Organização em camadas

- **controller**: registra as rotas HTTP e encaminha as requisições aos serviços.
- **services**: concentra a lógica de predição, consulta e estatísticas.
- **domain/dto**: define objetos de transferência de dados.
- **domain/repository**: executa as operações de persistência e consulta.
- **database**: encapsula a conexão e operações com SQLite.
- **utils**: contém utilitários para carregar o modelo, criar a pasta do banco e padronizar respostas HTTP.
- **resources**: contém o script SQL de criação das tabelas.
- **artifacts**: armazena o modelo treinado usado pela API.

## Pré-requisitos

- Python instalado (o projeto foi empacotado com arquivos de bytecode associados ao Python 3.12; a versão exata necessária não está declarada).
- `pip`.
- O arquivo `artifacts/modelo_iris.pkl` presente no caminho esperado.

## Instalação e execução

Execute os comandos a partir da raiz da pasta `backend/`.

1. Crie o ambiente virtual:

   **Windows:**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux/macOS:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   python -m pip install Flask Flask-Cors pandas joblib scikit-learn
   ```

3. Inicie a aplicação na porta **8080**:

   ```bash
   flask --app br/com/app/src/main/Main.py run --port 8080
   ```

Base URL local: `http://localhost:8080`

## Banco de dados

O banco utilizado é SQLite, armazenado em:

```text
database/database.db
```

São criadas duas tabelas:

### `request_data`

Armazena os atributos informados para a classificação:

- `id`
- `sepal_length`
- `sepal_width`
- `petal_length`
- `petal_width`

### `query_data`

Armazena o resultado da classificação:

- `id`
- `specie`
- `iris_setosa`
- `iris_versicolor`
- `iris_virginica`
- `query_date`
- `id_request_data` — referência ao registro de entrada em `request_data`.

## Endpoints

Todas as rotas usam o prefixo `/prediction`.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/prediction/predict` | Classifica uma flor e registra a consulta. |
| GET | `/prediction/all` | Lista classificações; aceita filtro opcional `specie`. |
| GET | `/prediction/{id}` | Consulta uma classificação pelo ID. |
| GET | `/prediction/stats` | Retorna estatísticas das classificações. |

### 1. Realizar classificação

**Requisição**

```http
GET http://localhost:8080/prediction/predict
Content-Type: application/json
```

Corpo JSON esperado:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Exemplo de resposta**

```json
{
  "species": "Iris Setosa",
  "probabilities": {
    "Iris Setosa": 0.98,
    "Iris Versicolor": 0.02,
    "Iris Virginica": 0.0
  }
}
```

Os valores acima são ilustrativos: a resposta real depende do modelo e das medidas enviadas. O código da rota está implementado como `GET` e obtém os dados por `request.get_json()`; portanto, o cliente precisa enviar o JSON no corpo da requisição. Para uma API convencional, recomenda-se avaliar a alteração dessa operação para `POST`.

### 2. Listar classificações

```http
GET http://localhost:8080/prediction/all
```

Para filtrar por espécie:

```http
GET http://localhost:8080/prediction/all?specie=Iris%20Setosa
```

Quando não há registros, o serviço retorna HTTP `404` com a mensagem `Predictions not found.`.

### 3. Consultar classificação por ID

```http
GET http://localhost:8080/prediction/1
```

O identificador é o ID do registro em `query_data`. Caso não seja encontrado, o serviço retorna HTTP `404`.

### 4. Consultar estatísticas

```http
GET http://localhost:8080/prediction/stats
```

A resposta contém os campos:

- `total_classifications`
- `setosa_count` e `setosa_percentage`
- `versicolor_count` e `versicolor_percentage`
- `virginica_count` e `virginica_percentage`

As porcentagens são calculadas sobre o total de classificações armazenadas.

## Respostas HTTP

A classe `ApiResponse` disponibiliza respostas padronizadas para os seguintes status:

| Status | Significado |
|---|---|
| `200` | Operação realizada com sucesso. |
| `201` | Recurso criado. |
| `400` | Requisição inválida. |
| `404` | Recurso não encontrado. |
| `409` | Conflito. |

As rotas atuais utilizam principalmente `200` e `404`; a existência dos demais métodos utilitários não significa que todos estejam associados a endpoints neste momento.

## Testes

O ZIP contém um diretório `test/`, mas não inclui arquivos de teste. Assim, não há uma suíte automatizada identificável no material enviado.

Para validar manualmente, inicie a API e execute as quatro chamadas descritas na seção **Endpoints**. Também é possível verificar a criação do arquivo `database/database.db` após a inicialização.

## Observações e pontos de atenção

- O arquivo do modelo é carregado durante a inicialização da aplicação. Se `artifacts/modelo_iris.pkl` não existir ou não puder ser desserializado, a aplicação não iniciará corretamente.
- Arquivos `.pkl`/Joblib devem ser carregados apenas quando forem confiáveis. Para evitar incompatibilidades, mantenha versões compatíveis das bibliotecas usadas no treinamento e na execução do modelo.
- O código de CORS configura recursos com o padrão `/note*`, enquanto as rotas da API usam `/prediction`. Se o frontend precisar acessar essas rotas de outra origem, revise essa configuração para corresponder ao prefixo efetivamente utilizado.
- A rota de predição está definida como `GET` com corpo JSON. A adoção de `POST` é recomendável para operações que recebem dados no corpo.
- Não há arquivo de dependências (`requirements.txt` ou equivalente) no conteúdo enviado. Recomenda-se criar um e registrar as versões testadas.

## Licença

Consulte o arquivo [LICENSE](LICENSE) para os termos de utilização e distribuição.
