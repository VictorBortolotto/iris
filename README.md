# Iris Classifier

Aplicação web de classificação supervisionada de flores do gênero **Iris**, desenvolvida utilizando técnicas de Machine Learning e uma arquitetura dividida em três componentes: **Classifier, Backend e Frontend**.

O sistema utiliza o Iris Dataset para treinar algoritmos de classificação, selecionar o modelo com melhor desempenho e disponibilizá-lo por meio de uma API REST. A aplicação web permite que os usuários informem as características de uma flor, visualizem a espécie prevista, consultem as probabilidades estimadas e acompanhem o histórico das classificações realizadas.

## Objetivos

### Objetivo geral

Desenvolver uma aplicação integrada de Machine Learning capaz de identificar espécies de flores do gênero Iris a partir de quatro características morfológicas: comprimento e largura das sépalas e comprimento e largura das pétalas.

### Objetivos específicos

- Utilizar o Iris Dataset como conjunto de dados para classificação supervisionada.
- Preparar, validar e dividir os dados em conjuntos de treinamento e teste.
- Treinar e comparar diferentes algoritmos de classificação.
- Otimizar hiperparâmetros utilizando validação cruzada.
- Avaliar o desempenho dos modelos por meio de métricas de classificação.
- Exportar o melhor modelo treinado para utilização posterior.
- Desenvolver uma API REST para disponibilizar as funcionalidades de classificação.
- Persistir os dados das classificações realizadas.
- Desenvolver uma interface web para interação com o sistema.
- Disponibilizar consultas de histórico e estatísticas das classificações.

## Arquitetura da aplicação

A aplicação está organizada em três componentes independentes, cada um com uma responsabilidade específica:

1. **Classifier:** responsável pelo processamento dos dados, treinamento, avaliação e exportação do modelo de Machine Learning.
2. **Backend:** responsável por carregar o modelo treinado, disponibilizar os serviços de classificação por meio de uma API REST e persistir os resultados.
3. **Frontend:** responsável pela interface de interação com o usuário e pela comunicação com o Backend.

Essa separação permite desenvolver, executar e manter cada componente de maneira independente, facilitando futuras evoluções da aplicação.

### Visão geral da arquitetura

```text
                  IRIS CLASSIFIER
                         |
          +--------------+--------------+
          |              |              |
          v              |              |
     CLASSIFIER          |              |
          |              |              |
          v              |              |
     Iris Dataset        |              |
          |              |              |
          v              |              |
    Pré-processamento    |              |
          |              |              |
          v              |              |
   Treinamento e         |              |
   validação dos modelos |              |
          |              |              |
          v              |              |
   Avaliação e seleção   |              |
          |              |              |
          v              |              |
   modelo_iris.pkl       |              |
          |              |              |
          v              |              |
     BACKEND             |              |
          |              |              |
   Carregamento do modelo|              |
          |              |              |
          v              |              |
    API REST <------------+             |
          |                             |
          v                             |
    Banco SQLite                        |
          ^                             |
          |                             |
          +---------- API REST <--------+
                         |
                         |
                      FRONTEND
                         |
                         v
                  Interface Web
                         |
                         v
                  Usuário final
```

### 1. Classifier — Machine Learning

O componente Classifier é responsável por todo o processo de construção e treinamento do modelo de Machine Learning.

Ele utiliza o Iris Dataset, disponibilizado pelo módulo `sklearn.datasets`, contendo 150 registros distribuídos entre três espécies:

- Iris Setosa.
- Iris Versicolor.
- Iris Virginica.

Cada registro possui quatro atributos:

| Atributo | Descrição |
|---|---|
| `sepal length (cm)` | Comprimento da sépala |
| `sepal width (cm)` | Largura da sépala |
| `petal length (cm)` | Comprimento da pétala |
| `petal width (cm)` | Largura da pétala |

O treinamento compara quatro algoritmos:

- **K-Nearest Neighbors (KNN):** classifica uma amostra considerando seus vizinhos mais próximos.
- **Decision Tree:** utiliza regras organizadas em uma estrutura de árvore.
- **Naive Bayes:** utiliza o teorema de Bayes para estimar a probabilidade das classes.
- **Support Vector Machine (SVM):** busca uma fronteira de decisão capaz de separar as classes.

A otimização dos hiperparâmetros é realizada com `GridSearchCV`, utilizando validação cruzada estratificada com cinco partições (`StratifiedKFold`).

Para KNN e SVM, são testados pipelines com normalização utilizando `StandardScaler` e `MinMaxScaler`.

Após o treinamento, os modelos são avaliados por meio das seguintes métricas:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Matriz de confusão.

O modelo com maior acurácia média na validação cruzada é selecionado e exportado utilizando Joblib.

O resultado é o arquivo:

`classifier/artifacts/modelo_iris.pkl`

Esse artefato contém o pipeline treinado, incluindo as etapas de pré-processamento, quando aplicáveis.

O Classifier também disponibiliza funções para carregar o modelo e realizar previsões individualmente, permitindo testar o artefato antes de sua integração com o Backend.

### 2. Backend — API REST

O Backend é responsável por disponibilizar as funcionalidades do modelo treinado por meio de uma API REST desenvolvida com Flask.

Diferentemente do Classifier, o Backend não realiza o treinamento dos algoritmos. Ele utiliza o arquivo `modelo_iris.pkl` previamente exportado para realizar as classificações.

Suas principais responsabilidades são:

- Carregar o modelo de Machine Learning durante a inicialização.
- Receber as características de uma flor por meio de requisições HTTP.
- Validar os dados recebidos.
- Realizar a classificação utilizando o modelo treinado.
- Retornar a espécie prevista e as probabilidades estimadas.
- Persistir os dados de entrada e os resultados no banco SQLite.
- Disponibilizar consultas ao histórico de classificações.
- Disponibilizar estatísticas das classificações realizadas.

O Backend utiliza uma organização em camadas:

| Camada | Responsabilidade |
|---|---|
| Controller | Recebe as requisições HTTP e encaminha as operações aos serviços. |
| Services | Implementa as regras de negócio e os processos de classificação e consulta. |
| Domain / DTO | Organiza os objetos utilizados para transferência de dados. |
| Domain / Repository | Responsável pelas operações de persistência e recuperação dos dados. |
| Database | Encapsula a conexão e as operações com SQLite. |
| Utils | Disponibiliza funções auxiliares e padronização de respostas. |
| Resources | Armazena scripts SQL utilizados na aplicação. |
| Artifacts | Armazena o modelo de Machine Learning treinado. |

O banco de dados SQLite armazena as informações em duas tabelas principais:

**request_data**

Armazena as características informadas pelo usuário:

- Identificador.
- Comprimento da sépala.
- Largura da sépala.
- Comprimento da pétala.
- Largura da pétala.

**query_data**

Armazena os resultados das classificações:

- Identificador.
- Espécie prevista.
- Probabilidade de Iris Setosa.
- Probabilidade de Iris Versicolor.
- Probabilidade de Iris Virginica.
- Data da consulta.
- Referência ao registro de entrada em `request_data`.

O relacionamento entre essas tabelas permite recuperar tanto as características utilizadas na classificação quanto o resultado produzido pelo modelo.

### 3. Frontend — Interface Web

O Frontend é responsável pela interação entre o usuário e a aplicação.

Desenvolvido utilizando HTML5, CSS3 e JavaScript, ele disponibiliza uma interface web para consumir os serviços do Backend.

O servidor web utiliza Node.js e Express para disponibilizar os arquivos estáticos e a página principal da aplicação.

Suas principais funcionalidades são:

- Informar as quatro características de uma flor.
- Solicitar uma classificação ao Backend.
- Visualizar a espécie prevista.
- Visualizar as probabilidades estimadas para cada espécie.
- Consultar estatísticas gerais das classificações.
- Consultar o histórico de classificações.
- Pesquisar classificações por espécie ou identificador.
- Navegar pelo histórico utilizando paginação.
- Exibir notificações de sucesso e erro.

A comunicação com o Backend é centralizada no arquivo `services.js`, responsável pelas requisições HTTP.

O Frontend não realiza o treinamento nem a classificação localmente. Todas as previsões e consultas dependem dos serviços disponibilizados pela API.

### Comunicação entre os componentes

O fluxo de integração acontece da seguinte maneira:

1. O Classifier carrega o Iris Dataset e executa o treinamento dos algoritmos.
2. Após a avaliação, seleciona o melhor modelo e exporta o arquivo `modelo_iris.pkl`.
3. O artefato é disponibilizado na pasta `artifacts` do Backend.
4. O Backend carrega o modelo durante sua inicialização.
5. O usuário acessa a interface web disponibilizada pelo Frontend.
6. Ao informar as características de uma flor, o Frontend envia uma requisição HTTP para o Backend.
7. O Backend utiliza o modelo carregado para realizar a classificação.
8. O resultado e as probabilidades são retornados ao Frontend.
9. O Backend persiste os dados de entrada e o resultado no banco SQLite.
10. O Frontend utiliza os endpoints de consulta para apresentar o histórico e as estatísticas.

Dessa maneira, o treinamento do modelo acontece independentemente da execução da aplicação web. Novas versões do modelo podem ser treinadas e disponibilizadas ao Backend sem modificar o fluxo de interação do usuário.

## Tecnologias utilizadas

| Tecnologia | Componente | Finalidade |
|---|---|---|
| Python | Classifier / Backend | Linguagem de programação |
| Scikit-learn | Classifier / Backend | Treinamento, pré-processamento e inferência |
| Pandas | Classifier / Backend | Manipulação de dados |
| NumPy | Classifier | Operações numéricas |
| Matplotlib | Classifier | Geração de gráficos |
| Seaborn | Classifier | Visualização de matrizes de confusão |
| Joblib | Classifier / Backend | Serialização e carregamento do modelo |
| Flask | Backend | Desenvolvimento da API REST |
| Flask-CORS | Backend | Configuração de acesso entre origens |
| SQLite | Backend | Persistência dos dados |
| HTML5 | Frontend | Estrutura da interface |
| CSS3 | Frontend | Estilização da aplicação |
| JavaScript | Frontend | Interações e comunicação com a API |
| Node.js | Frontend | Ambiente de execução do servidor web |
| Express | Frontend | Disponibilização dos arquivos estáticos |
| Git | Projeto | Controle de versão |

## Estrutura do projeto

A estrutura geral do repositório está organizada da seguinte maneira:

```text
iris-classifier/
│
├── classifier/
│   ├── artifacts/
│   │   └── modelo_iris.pkl
│   ├── reports/
│   │   ├── figures/
│   │   └── results/
│   ├── scripts/
│   │   └── deploy_model.py
│   ├── src/
│   │   ├── data/
│   │   ├── evaluation/
│   │   ├── export/
│   │   ├── models/
│   │   ├── prediction/
│   │   ├── preprocessing/
│   │   └── training/
│   ├── main.py
│   ├── prediction_test.py
│   └── requirements.txt
│
├── backend/
│   ├── artifacts/
│   │   └── modelo_iris.pkl
│   ├── br/
│   │   └── com/app/src/
│   │       ├── main/
│   │       │   ├── controller/
│   │       │   ├── database/
│   │       │   ├── domain/
│   │       │   ├── services/
│   │       │   ├── utils/
│   │       │   └── Main.py
│   │       └── resources/
│   ├── database/
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── server.js
│   │   └── public/
│   │       ├── assets/
│   │       ├── css/
│   │       ├── js/
│   │       └── page/
│   ├── package.json
│   └── package-lock.json
│
└── README.md
```

*Observação: arquivos e diretórios internos foram agrupados para facilitar a visualização da arquitetura.*

## Pré-requisitos

Antes de executar a aplicação, é necessário possuir:

- Python 3.10 ou superior.
- pip.
- Node.js e npm.
- Git (opcional, para clonar o repositório).

Recomenda-se utilizar ambientes virtuais Python para manter as dependências isoladas.

Também é necessário garantir que as versões do Scikit-learn utilizadas no treinamento e na execução do modelo sejam compatíveis.

## Instalação e configuração

A instalação deve ser realizada individualmente para cada componente.

### 1. Obter o projeto

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd iris-classifier
```

Substitua `<URL_DO_REPOSITORIO>` pelo endereço do repositório Git.

### 2. Configurar o Classifier

Acesse a pasta:

```bash
cd classifier
```

Crie e ative o ambiente virtual.

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém:

```text
pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
```

### 3. Executar o treinamento

Na raiz da pasta `classifier`, execute:

```bash
python main.py
```

O processo realizará:

1. Carregamento e validação do Iris Dataset.
2. Separação dos dados em treinamento e teste.
3. Construção dos pipelines de classificação.
4. Otimização dos hiperparâmetros.
5. Avaliação dos algoritmos.
6. Geração dos relatórios e matrizes de confusão.
7. Seleção do melhor modelo.
8. Exportação do modelo treinado.

O arquivo gerado será:

```text
classifier/artifacts/modelo_iris.pkl
```

Opcionalmente, execute o teste de predição:

```bash
python prediction_test.py
```

### 4. Disponibilizar o modelo no Backend

Após o treinamento, é necessário copiar o modelo exportado para o diretório de artefatos do Backend.

Na pasta `classifier`, execute:

```bash
python scripts/deploy_model.py
```

O script realizará a cópia:

```text
classifier/artifacts/modelo_iris.pkl
```

Para:

```text
backend/artifacts/modelo_iris.pkl
```

O script pressupõe que as pastas `classifier` e `backend` estejam no mesmo nível hierárquico.

**Importante:** execute o treinamento antes da cópia. O script de deploy não treina nem modifica o modelo, apenas disponibiliza o artefato no Backend.

### 5. Configurar o Backend

Acesse a pasta:

```bash
cd ../backend
```

Crie e ative um ambiente virtual.

**Windows:**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install Flask Flask-Cors pandas joblib scikit-learn
```

O Backend utiliza:

- Flask.
- Flask-CORS.
- Pandas.
- Joblib.
- Scikit-learn.

Inicie a API:

```bash
flask --app br/com/app/src/main/Main.py run --port 8080
```

A API ficará disponível em:

```text
http://localhost:8080
```

O banco SQLite será criado automaticamente durante a inicialização, no caminho:

```text
backend/database/database.db
```

### 6. Configurar o Frontend

Acesse a pasta:

```bash
cd ../frontend
```

Instale as dependências:

```bash
npm install
```

O projeto utiliza o Express como dependência para disponibilizar a interface web.

Inicie o servidor:

```bash
node src/server.js
```

A aplicação ficará disponível em:

```text
http://localhost:3000
```

**Importante:** o Backend deve estar em execução para que as funcionalidades de classificação, histórico e estatísticas estejam disponíveis.

## Endpoints da API

O Backend disponibiliza os serviços de classificação e consulta por meio do prefixo:

```text
http://localhost:8080/prediction
```

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/prediction/predict` | Realiza a classificação de uma flor. |
| GET | `/prediction/all` | Lista as classificações realizadas. |
| GET | `/prediction/all?specie={espécie}` | Lista classificações filtradas por espécie. |
| GET | `/prediction/{id}` | Consulta uma classificação pelo identificador. |
| GET | `/prediction/stats` | Retorna estatísticas das classificações. |

### Exemplo de classificação

Requisição:

```http
POST http://localhost:8080/prediction/predict
Content-Type: application/json
```

Corpo:

```json
{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
```

Exemplo de resposta:

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

Os valores apresentados são ilustrativos e dependem do modelo treinado e das características informadas.

### Consulta de histórico

Para recuperar todas as classificações:

```http
GET http://localhost:8080/prediction/all
```

Para filtrar por espécie:

```http
GET http://localhost:8080/prediction/all?specie=Iris%20Setosa
```

### Consulta por identificador

```http
GET http://localhost:8080/prediction/1
```

### Consulta de estatísticas

```http
GET http://localhost:8080/prediction/stats
```

A resposta disponibiliza:

- Total de classificações.
- Quantidade de ocorrências de Iris Setosa.
- Percentual de Iris Setosa.
- Quantidade de ocorrências de Iris Versicolor.
- Percentual de Iris Versicolor.
- Quantidade de ocorrências de Iris Virginica.
- Percentual de Iris Virginica.

As consultas de histórico e estatísticas consideram os registros persistidos no banco SQLite.

## Execução completa da aplicação

Para executar a aplicação integrada, siga a ordem abaixo:

| Ordem | Componente | Operação |
|---|---|---|
| 1 | Classifier | Instalar dependências e treinar o modelo. |
| 2 | Classifier | Executar o deploy do artefato para o Backend. |
| 3 | Backend | Instalar dependências e iniciar a API na porta 8080. |
| 4 | Frontend | Instalar dependências e iniciar o servidor na porta 3000. |
| 5 | Aplicação | Acessar a interface pelo navegador. |

Com todos os componentes em execução, acesse:

```text
http://localhost:3000
```

O usuário poderá informar as medidas de uma flor, solicitar sua classificação e consultar os resultados armazenados.

## Observações técnicas

- O Classifier e o Backend são aplicações Python independentes e podem utilizar ambientes virtuais separados.
- O Frontend possui seu próprio gerenciamento de dependências por meio do npm.
- O treinamento do modelo não precisa ser executado a cada inicialização do Backend.
- O arquivo `modelo_iris.pkl` precisa estar disponível no caminho esperado pelo Backend.
- O modelo exportado contém o pipeline de pré-processamento e classificação, quando aplicável.
- Modelos serializados com Joblib podem apresentar incompatibilidades entre versões diferentes de bibliotecas. Mantenha versões compatíveis de Python e Scikit-learn.
- O Frontend utiliza a URL `http://localhost:8080/prediction` como endereço padrão da API. Caso o Backend seja executado em outro endereço, atualize a constante `DEFAULT_URL` em `frontend/src/public/js/services.js`.
- Como o Frontend e o Backend utilizam portas diferentes, é necessário configurar corretamente o CORS para permitir a comunicação entre eles.
- Recomenda-se manter um arquivo `requirements.txt` também no Backend, registrando as versões efetivamente testadas.
- A rota de classificação deve utilizar POST, pois recebe características da flor no corpo da requisição. É necessário garantir que o método HTTP implementado no Backend esteja alinhado ao utilizado pelo Frontend.

## Possíveis evoluções

A arquitetura permite futuras melhorias e extensões, como:

- Disponibilização de novos algoritmos de Machine Learning.
- Treinamento com conjuntos de dados adicionais.
- Implementação de autenticação e autorização.
- Utilização de bancos de dados mais robustos.
- Disponibilização da aplicação em ambiente de produção.
- Containerização dos componentes utilizando Docker.
- Implementação de testes automatizados.
- Monitoramento do desempenho do modelo em produção.
- Versionamento dos modelos de Machine Learning.

## Licença

Consulte o arquivo `LICENSE` para obter as informações sobre licenciamento, utilização e distribuição do projeto.