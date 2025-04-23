# Challenge GraphQL & NLP API

API con servicios GraphQL y procesamiento de lenguaje natural para análisis de datos de CSV sobre ventas.

## Características

- Servicio de datos con acceso a CSV por medio de un insert a Postgresql y consultas SQL a esta base de datos
- Endpoint GraphQL
- Endpoint NLP para consultas en lenguaje natural
- Documentación Swagger
- Autenticación OAuth 2.0 

## Requisitos

- Docker
- Docker Compose

## Configuración

1. Configura variables de entorno (`.env`):
```bash
PG_USER=tu_usuario
PG_PASSWORD=tu_password
PG_DATABASE=tu_db_name

KEYCLOAK_REALM=tu_realm
KEYCLOAK_CLIENT_ID=tu_client_id
KEYCLOAK_CLIENT_SECRET=tu_client_secret
KEYCLOAK_URL=https://auth.juanluisacebal.com

OPENAI_API_KEY=tu_api_key

```

### Carga de datos CSV

Antes de iniciar la API, puedes descargar el CSV, sino, tomará el siguiente:
    [Descargar CSV de ejemplo](https://file.notion.so/f/f/8bdb40ef-cc0d-4853-862c-95ff2b4790ca/b82763a3-3ac0-4c8a-99bb-d763c0b00b54/Data_example_-_Python_Coding_Challenge_-_GraphQL.csv?table=block&id=3e5c15a8-875d-43ae-b866-c1515de08c01&spaceId=8bdb40ef-cc0d-4853-862c-95ff2b4790ca&expirationTimestamp=1745366400000&signature=AmH4rnK8MxZKqA66BRo-5RvzpY1K29pBns_AHzmf_3w&downloadName=Data+example+-+Python+Coding+Challenge+-+GraphQL.csv)

Lo tienes que dejar en files/
Sino, tomará el del repositorio.

## Desarrollo

Inicia los servicios:
```bash
git clone git@github.com:juanluisacebal/challenge_graphql_nlp_api.git
cd challenge_graphql_nlp_api
docker compose up --build
docker compose -f docker/docker-compose.yml up 
```

La API estará disponible en:
- API: `http://localhost:8000`
- Documentación: `http://localhost:8000/docs`
- GraphiQL: `http://localhost:8000/graphql`


## Endpoints

- GraphQL: `/graphql`
  - Interfaz GraphiQL disponible para dev
  - Requiere token Bearer para consultas
- REST API:
  - `/api/data`: Endpoints para datos
  - `/api/nlp`: Procesamiento de lenguaje natural

## Estructura

```
src/
├── api/
│   ├── data_service/
│   ├── graphql_service/
│   └── nlp_service/
└── core/
```

## Autenticación
Usa Keycloak para autenticación. Incluye el token en los headers:
```
Authorization: Bearer <token>
```