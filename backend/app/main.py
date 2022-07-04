from fastapi import FastAPI

from core__database import add_database
from core__errors_handlers import add_error_handlers
from core__middlewares import add_middlewares
from core__routes import add_routes


app = FastAPI()

@app.get("/")
def get_root():
  return dict(message="Welcome. Lemmario's API")

############################################################################
# DATABASE
############################################################################
add_database()


############################################################################
# ROUTES
############################################################################
add_routes(app)


############################################################################
# MIDDLEWARES
############################################################################
add_middlewares(app)


############################################################################
# EXCEPTION HANDLERS
############################################################################
add_error_handlers(app)
