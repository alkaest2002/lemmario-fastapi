
from fastapi import FastAPI

from starlette.responses import JSONResponse
from fastapi import Request, status
from sqlalchemy.exc import IntegrityError


def add_error_handlers(app: FastAPI):

  @app.exception_handler(IntegrityError)
  async def sqlalchemy_integrity_error(request: Request, excepion: IntegrityError):
    return JSONResponse(content=dict(detail="database unique integrity error"), status_code=status.HTTP_400_BAD_REQUEST)
