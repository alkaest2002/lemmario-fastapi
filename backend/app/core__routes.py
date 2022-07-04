from fastapi import FastAPI

import routes__lemmi
import routes__users
import routes__scrape

def add_routes(app: FastAPI):
  for routes in [routes__lemmi, routes__users, routes__scrape]:
    app.include_router(routes.router)