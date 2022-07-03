import re

from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, status, HTTPException
from sqlalchemy.exc import IntegrityError
from core__security import JWTBearer

from database__init_db import engine
from models__lemmi import Base

import routes__lemmi
import routes__users
import routes__scrape

Base.metadata.create_all(engine)

app = FastAPI()

############################################################################
# ROUTES
############################################################################

app.include_router(routes__lemmi.router)
app.include_router(routes__users.router)
app.include_router(routes__scrape.router)


@app.get("/")
def get_root(): return {"message": "Welcome. Lemmario's API"}


############################################################################
# MIDDLEWARE
############################################################################

@app.middleware("http")
async def add_security(request: Request, call_next):
  if not re.search('login', request.url.path):
    token = JWTBearer()
    try:
      await token.__call__(request)
    except HTTPException as err:
      return JSONResponse(content=dict(detail=err.detail), status_code=err.status_code)
    except Exception as err:
      return JSONResponse(content=dict(detail=str(err)), status_code=status.HTTP_400_BAD_REQUEST)
      
  return await call_next(request)


############################################################################
# GLOBAL EXCEPTION HANDLERS
############################################################################

@app.exception_handler(IntegrityError)
async def sqlalchemy_integrity_error(request: Request, excepion: IntegrityError):
  return JSONResponse(content=dict(detail="database unique integrity error"), status_code=status.HTTP_400_BAD_REQUEST)
