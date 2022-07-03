from fastapi import FastAPI

from core__database import set_database
from core__errors_handlers import set_errors_handlers
from core__middlewares import set_middlewares
from core__routes import set_routes


app = FastAPI()

@app.get("/")
def get_root():
  return dict(message="Welcome. Lemmario's API")

############################################################################
# DATABASE
############################################################################
set_database()


############################################################################
# ROUTES
############################################################################
set_routes(app)


############################################################################
# MIDDLEWARES
############################################################################
set_middlewares(app)


############################################################################
# EXCEPTION HANDLERS
############################################################################
set_errors_handlers(app)
