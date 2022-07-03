from fastapi import FastAPI

from database__init_db import engine
from models__lemmi import Base

from core__errors_handlers import set_errors_handlers
from core__middlewares import set_middlewares

import routes__lemmi
import routes__users
import routes__scrape

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def get_root(): return {"message": "Welcome. Lemmario's API"}


############################################################################
# ROUTES
############################################################################
for routes in [routes__lemmi, routes__users, routes__scrape]:
  app.include_router(routes.router)


############################################################################
# MIDDLEWARES
############################################################################
set_middlewares(app)


############################################################################
# EXCEPTION HANDLERS
############################################################################
set_errors_handlers(app)