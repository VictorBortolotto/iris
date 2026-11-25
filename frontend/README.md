# Iris Classifier — Frontend

Aplicação web desenvolvida para interagir com um sistema de classificação de espécies de flores do conjunto **Iris**. A interface permite informar as medidas de uma flor, solicitar uma predição ao backend, visualizar estatísticas das classificações e consultar o histórico de consultas realizadas.

## Funcionalidades

- **Classificação de flores:** envio das medidas de sépala e pétala para obter a espécie prevista.
- **Probabilidades:** apresentação das probabilidades retornadas pelo backend para cada espécie.
- **Estatísticas:** exibição do total de classificações e da quantidade e percentual de ocorrências de cada espécie.
- **Histórico:** consulta das classificações realizadas anteriormente.
- **Pesquisa no histórico:** busca por espécie ou pelo identificador de uma classificação.
- **Paginação:** navegação entre as páginas de resultados do histórico.
- **Notificações:** mensagens de retorno para operações bem-sucedidas ou situações de erro.

As espécies consideradas pela interface são:

- Iris Setosa
- Iris Versicolor
- Iris Virginica

## Tecnologias utilizadas

- **HTML5** — estrutura da interface.
- **CSS3** — estilos e apresentação visual.
- **JavaScript** — interações, manipulação da interface e comunicação com a API.
- **Node.js** — ambiente de execução do servidor.
- **Express** — disponibilização dos arquivos estáticos e da página inicial.

## Estrutura do projeto

```text
frontend/
├── package.json
├── package-lock.json
├── LICENSE
├── README.md
└── src/
    ├── server.js
    └── public/
        ├── assets/
        │   ├── iris_logo.png
        │   ├── not_found.png
        │   ├── next.svg
        │   └── previous.svg
        ├── css/
        │   ├── components.css
        │   ├── index.css
        │   └── snackbar.css
        ├── js/
        │   ├── component/
        │   │   └── card.component.js
        │   ├── page.js
        │   ├── services.js
        │   └── snackbar.js
        └── page/
            └── index.html
```

### Organização dos principais arquivos

| Arquivo | Responsabilidade |
|---|---|
| `src/server.js` | Inicializa o servidor Express, disponibiliza os arquivos estáticos e configura a rota principal. |
| `src/public/page/index.html` | Contém a estrutura HTML da aplicação. |
| `src/public/js/services.js` | Centraliza as requisições HTTP realizadas para o backend. |
| `src/public/js/page.js` | Implementa os comportamentos da página, como predição, estatísticas, histórico, pesquisa e paginação. |
| `src/public/js/component/card.component.js` | Gera o HTML dos itens apresentados no histórico. |
| `src/public/js/snackbar.js` | Implementa as notificações exibidas na interface. |
| `src/public/css/` | Contém os estilos da aplicação. |
| `src/public/assets/` | Armazena imagens e ícones utilizados pela interface. |

## Pré-requisitos

Antes de executar a aplicação, é necessário ter instalado:

- [Node.js](https://nodejs.org/) e npm.
- O backend do projeto Iris Classifier em execução e acessível pela URL `http://localhost:8080/prediction`.

> **Importante:** o frontend não realiza a classificação localmente. As predições, estatísticas e consultas ao histórico dependem da API disponibilizada pelo backend.

## Instalação e execução

### 1. Acesse a pasta do frontend

```bash
cd frontend
```

### 2. Instale as dependências

```bash
npm install
```

Atualmente, o projeto utiliza o Express como dependência para executar o servidor web.

### 3. Inicie o servidor

```bash
node src/server.js
```

Após a inicialização, o terminal deverá apresentar:

```text
Servidor rodando em http://localhost:3000
```

### 4. Acesse a aplicação

Abra o navegador e acesse:

[http://localhost:3000](http://localhost:3000)

## Integração com o backend

As requisições HTTP são centralizadas no arquivo `src/public/js/services.js`.

A URL base configurada atualmente é:

```text
http://localhost:8080/prediction
```

A interface utiliza os seguintes endpoints:

| Método | Endpoint | Finalidade |
|---|---|---|
| `POST` | `/predict` | Envia as medidas da flor e solicita uma classificação. |
| `GET` | `/stats` | Recupera as estatísticas das classificações. |
| `GET` | `/all` | Recupera o histórico de classificações. |
| `GET` | `/all?specie={espécie}` | Filtra o histórico por espécie. |
| `GET` | `/{id}` | Recupera uma classificação pelo identificador. |

### Dados enviados para classificação

A requisição `POST /predict` envia um objeto JSON com as quatro medidas da flor:

```json
{
  "sepal_length": 5.9,
  "sepal_width": 3.0,
  "petal_length": 4.2,
  "petal_width": 1.5
}
```

A interface utiliza a resposta da classificação para apresentar:

- A espécie prevista (`species`).
- A probabilidade de Iris Setosa.
- A probabilidade de Iris Versicolor.
- A probabilidade de Iris Virginica.

### Resposta de estatísticas

A interface espera que o endpoint `/stats` retorne os dados dentro da propriedade `data`, incluindo:

- `total_classifications`
- `setosa_count` e `setosa_percentage`
- `versicolor_count` e `versicolor_percentage`
- `virginica_count` e `virginica_percentage`

### Histórico de classificações

O histórico é utilizado para apresentar os dados de cada consulta, incluindo espécie prevista, data da consulta, probabilidades e medidas informadas.

A interface também espera que as respostas dos endpoints de histórico disponibilizem os dados na propriedade `data`.

> Os formatos acima descrevem os campos consumidos pelo frontend. Consulte a documentação ou a implementação do backend para verificar o contrato completo das respostas da API.

## Configuração da API

Caso o backend esteja sendo executado em outro endereço ou porta, altere a constante `DEFAULT_URL` no arquivo:

```text
src/public/js/services.js
```

Exemplo:

```javascript
const DEFAULT_URL = "http://localhost:8080/prediction";
```

Como o frontend é servido na porta `3000` e a API utiliza a porta `8080`, o backend precisa permitir requisições de origem cruzada (**CORS**) para a origem do frontend.

## Observações

- O servidor Express disponibiliza os arquivos da pasta `src/public`.
- A rota `/` entrega a página `src/public/page/index.html`.
- O servidor frontend utiliza a porta `3000`, configurada diretamente em `src/server.js`.
- A URL da API também está configurada diretamente no código JavaScript.
- O `package.json` ainda não possui um script de inicialização; por isso, a execução é feita diretamente pelo comando `node src/server.js`.
- Não há uma rotina de testes automatizados configurada no `package.json` atualmente.

## Licença

Consulte o arquivo [LICENSE](LICENSE) para obter as informações sobre a licença do projeto.
