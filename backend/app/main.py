from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from data.database.models import lemmi as models
from data.database.db_init import engine

from routers import lemmi as routes_lemmi
from routers import users as routes_users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes_lemmi.router)
app.include_router(routes_users.router)

@app.get("/")
def get_root():
  return {
    "welcome": "lemmario api"
  }

