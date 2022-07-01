from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, status
from sqlalchemy.exc import IntegrityError

from database__init_db import engine
from models__lemmi import Base

import routes__lemmi
import routes__users

Base.metadata.create_all(engine)

app = FastAPI()

############################################################################
# ROUTES
############################################################################

app.include_router(routes__lemmi.router)
app.include_router(routes__users.router)

@app.get("/")
def get_root(): return { "message": "Welcome. Lemmario's API" }


############################################################################
# GLOBAL EXCEPTION HANDLERS
############################################################################

@app.exception_handler(IntegrityError)
async def sqlalchemy_integrity_error(request: Request, excepion: IntegrityError):
  return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "database unique integrity error"})