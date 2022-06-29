from inspect import getargs
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependency__db import get_db
from core__security import JWTBearer
from core_enums import FieldEnum, PageDirEnum, OrderDirEnum

import crud__lemmi as Tbl
from schemas__lemmi import LemmaOut
from scrape_lemmi import Scaprer

router = APIRouter(prefix="/lemmi",)


@router.get("", response_model=LemmaOut)
async def get_lemmi(
	offset: int | str | None = None, 
	order_by: FieldEnum = FieldEnum.lemma,
	order_dir: OrderDirEnum = OrderDirEnum.asc,
	page_dir: PageDirEnum = PageDirEnum.next,
	page_size: int = 5, 
	db: Session = Depends(get_db), 
	_: str = Depends(JWTBearer())
):
	lemmi = Tbl.get_lemmi(
		db=db, 
		offset=offset, 
		order_by=order_by,
		order_dir=order_dir,
		page_dir=page_dir, 
		page_size=page_size+1,
	)
	data_to_return = dict(
		data=lemmi, 
		metadata=dict(
			offset=offset if len(lemmi) == page_size+1 else None,
			order_by=order_by,
			order_dir=order_dir,
			page_dir=page_dir,
			page_size=page_size
		)
	)
	return data_to_return
	
@router.get("/{lemma}")
async def get_lemma(lemma: str, db: Session = Depends(get_db), _: str = Depends(JWTBearer())):
	lemma = Tbl.get_lemma(db=db, lemma=lemma)
	return lemma

@router.get("/search/{lemma}")
async def search_lemma(lemma: str, _: str = Depends(JWTBearer())):
	scraper = Scaprer(lemma)
	return scraper.scrape()
