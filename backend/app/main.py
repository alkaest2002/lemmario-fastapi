from fastapi import FastAPI

from database__init_db import engine
from models__lemmi import Base

import routes__lemmi
import routes__users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes__lemmi.router)
app.include_router(routes__users.router)

@app.get("/")
def get_root():
  return {
    "message": "Welcome. Lemmario's API"
  }

