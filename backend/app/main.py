from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL
from app.routes import routing, ai, auth, user_routes
from app.routes.graph import schema
from app.database import init_db

app = FastAPI(title="Cartograph API", version="0.1.0")

# Initialize database
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user_routes.router)
app.include_router(routing.router)
app.include_router(ai.router)
app.add_route("/graphql", GraphQL(schema))

@app.get("/health")
def health():
    return {"status": "ok"}
