from inspect import getargs
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependency__db import get_db
from core__security import JWTBearer
from core_enums import FieldEnum, PageDirEnum, OrderDirEnum

import crud__lemmi as Tbl

router = APIRouter(prefix="/lemmi",)


@router.get("")
async def get_lemmi(
	offset: int | str | None = None, 
	page_size: int = 5, 
	page_dir: PageDirEnum = PageDirEnum.next,
	order_by: FieldEnum = FieldEnum.lemma,
	order_dir: OrderDirEnum = OrderDirEnum.asc,
	db: Session = Depends(get_db), 
	_: str = Depends(JWTBearer())
):
	lemmi = Tbl.get_lemmi(
		db=db, 
		offset=offset, 
		order_by=order_by,
		order_dir=order_dir,
		page_size=page_size+1,
		page_dir=page_dir, 
	)
	data_to_return = dict(
		data=lemmi, 
		metadata=dict(
			offset=offset if len(lemmi) == page_size+1 else None,
			order_by=order_by,
			order_dir=order_dir,
			page_size=page_size,
			page_dir=page_dir
		)
	)
	return data_to_return
	
@router.get("/{lemma}")
async def get_lemma(lemma: str, db: Session = Depends(get_db), _: str = Depends(JWTBearer())):
	lemma = Tbl.get_lemma(db=db, lemma=lemma)
	return lemma
