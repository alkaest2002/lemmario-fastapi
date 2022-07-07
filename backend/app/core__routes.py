from fastapi import FastAPI

import routes__lemmi
import routes__users
import routes__scrape

def add_routes(app: FastAPI):
  for routes, tags in [
    (routes__users, ["users"]),
    (routes__lemmi, ["lemmi"]), 
    (routes__scrape, ["scrape"]),
  ]:
    app.include_router(routes.router, tags=tags)