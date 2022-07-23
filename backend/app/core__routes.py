from fastapi import FastAPI

import routes__lemmi
import routes__users
import routes__treccani

def add_routes(app: FastAPI):
  for routes, tags in [
    (routes__users, ["users"]),
    (routes__lemmi, ["lemmi"]), 
    (routes__treccani, ["scrape"]),
  ]:
    app.include_router(routes.router, tags=tags)