from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL
from app.routes import routing
from app.routes.graph import schema

app = FastAPI(title="Cartograph API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routing.router)
app.add_route("/graphql", GraphQL(schema))

@app.get("/health")
def health():
    return {"status": "ok"}
