from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependency__db import get_db
from core_enums import FieldEnum, PageDirEnum, OrderDirEnum

import crud__lemmi as lemmi_crud
from models__lemmi import LemmaModel
from schemas__lemmi import LemmaSchema, LemmaListSchema

router = APIRouter(prefix="/lemmi",)


@router.get("/list", response_model=LemmaListSchema)
async def get_lemmi(
	offset: int | str | None = None,
	order_by: FieldEnum = FieldEnum.lemma,
	order_dir: OrderDirEnum = OrderDirEnum.asc,
	page_dir: PageDirEnum = PageDirEnum.next,
	page_size: int = 5,
	db: Session = Depends(get_db),
):
	lemmi = lemmi_crud.get_lemmi(
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


@router.get("/view/{lemma}")
async def get_lemma(lemma: str, db: Session = Depends(get_db)):
	lemma = lemmi_crud.get_lemma(db=db, lemma=lemma)
	return lemma


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_lemma(*, lemma: LemmaSchema, db: Session = Depends(get_db)) -> LemmaModel:
	lemma = lemmi_crud.create_lemma(db=db, lemma=lemma)
	return lemma
