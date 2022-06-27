from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependency__db import get_db
from core__security import JWTBearer

import crud__lemmi as Tbl

router = APIRouter(prefix="/lemmi",)

@router.get("")
async def get_lemmi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: str = Depends(JWTBearer())):
	lemmi = Tbl.get_lemmi(db, skip=skip, limit=limit)
	return lemmi
	
@router.get("/{lemma}")
async def get_lemma(lemma: str, db: Session = Depends(get_db), _: str = Depends(JWTBearer())):
	lemma = Tbl.get_lemma(db, lemma)
	return lemma
