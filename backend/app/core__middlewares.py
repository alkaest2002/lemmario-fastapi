
import re

from starlette.responses import JSONResponse
from fastapi import Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core__security import JWTBearer

def set_middlewares(app):

  app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      "http://localhost",
      "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  @app.middleware("http")
  async def add_security(request: Request, call_next):
    if not re.search('login', request.url.path):
      try:
        token = JWTBearer()
        await token.__call__(request)
      except HTTPException as err:
        return JSONResponse(content=dict(detail=err.detail), status_code=err.status_code)
      except Exception as err:
        return JSONResponse(content=dict(detail=str(err)), status_code=status.HTTP_400_BAD_REQUEST)
    return await call_next(request)