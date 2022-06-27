from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas__tokens import TokenSchema

from core__security import (TokenMaker, PasswordManager)

from core__config import settings

router = APIRouter(prefix="/utenti",)

@router.post('/login', response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  
  # unpack data
  (username, password) = (form_data.username, form_data.password)
  (admin_email, admin_password) = (settings.ADMIN_EMAIL, settings.ADMIN_HASHED_PASS)
  
  # verify email
  if username != admin_email:
    raise HTTPException(
      status_code=status.status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email"
    )
  
  # verify password
  if not PasswordManager().verify_password(password, admin_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect password"
    )
  
  # create token maker
  token_maker = TokenMaker(username)

  return {
    "access_token": token_maker.create_access_token(),
    "refresh_token": token_maker.create_refresh_token(),
  }