from fastapi import FastAPI
from app.api.routes.route_user import routes as users_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # ✔️ aggiunto
    allow_headers=["*"],
)

app.include_router(users_router)
