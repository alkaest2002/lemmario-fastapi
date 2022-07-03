
from starlette.responses import JSONResponse
from fastapi import Request, status
from sqlalchemy.exc import IntegrityError


def set_errors_handlers(app):

  @app.exception_handler(IntegrityError)
  async def sqlalchemy_integrity_error(request: Request, excepion: IntegrityError):
    return JSONResponse(content=dict(detail="database unique integrity error"), status_code=status.HTTP_400_BAD_REQUEST)
