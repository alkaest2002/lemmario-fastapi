from fastapi import FastAPI

import routes__lemmi
import routes__users
import routes__scrape_treccani
import routes__scrape_hoepli

def add_routes(app: FastAPI):
  for routes, tags in [
    (routes__users, ["users"]),
    (routes__lemmi, ["lemmi"]), 
    (routes__scrape_treccani, ["scrape"]),
    (routes__scrape_hoepli, ["scrape"]),
  ]:
    app.include_router(routes.router, tags=tags)