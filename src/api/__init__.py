from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from .data_service.routes import router as data_router
from .nlp_service.routes import router as nlp_router
from .graphql_service.schema import schema
from ..core.init_db import init_db

app = FastAPI(
    title="Challenge GraphQL & NLP API",
    description="API con servicios GraphQL y NLP para análisis de datos",
    version="0.1.9"
)

# Inicializar base de datos
init_db()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(data_router, prefix="/api/data", tags=["Data Service"])
app.include_router(nlp_router, prefix="/api/nlp", tags=["NLP Service"])

# GraphQL
graphql_app = GraphQLRouter(
    schema,
    context_getter=lambda request: {"request": request}
)
app.include_router(graphql_app, prefix="/graphql", tags=["GraphQL"])

@app.get("/")
async def root():
    return {"message": "Challenge GraphQL & NLP API"} 