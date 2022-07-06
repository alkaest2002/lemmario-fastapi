from fastapi import APIRouter, Depends, status
from pydantic import constr
from sqlalchemy.orm import Session

from dependency__db import get_db
from core_enums import FieldEnum, PageDirEnum, OrderDirEnum

import crud__lemmi as lemmi_crud
from models__lemmi import LemmaModel, LemmaFullTextSerachModel
from schemas__lemmi import LemmaSchema, LemmaListSchema

router = APIRouter(prefix="/lemmi")


@router.get("/list", response_model=LemmaListSchema)
async def list_lemmi(
	offset: int | str | None = None,
	order_by: FieldEnum = FieldEnum.lemma,
	order_dir: OrderDirEnum = OrderDirEnum.asc,
	page_dir: PageDirEnum = PageDirEnum.next,
	page_size: int = 5,
	db: Session = Depends(get_db),
) -> LemmaListSchema:
	lemmi = lemmi_crud.list_lemmi(
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


@router.get("/view/{lemma_id}")
async def view_lemma(lemma_id: int, db: Session = Depends(get_db)) -> LemmaModel:
	return lemmi_crud.view_lemma(db=db, lemma_id=lemma_id)


@router.get("/search/{lemma}")
async def search_lemma(lemma: constr(min_length=3), exact: bool = False, db: Session = Depends(get_db)) -> list[LemmaFullTextSerachModel]:
	return lemmi_crud.search_lemma(db=db, lemma=lemma, exact=exact)
	

@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_lemma(*, lemma: LemmaSchema, db: Session = Depends(get_db)) -> LemmaModel:
	return lemmi_crud.insert_lemma(db=db, lemma=lemma)


@router.put("/update/{lemma_id}")
async def update_lemma(*, lemma_id: int, lemma: LemmaSchema, db: Session = Depends(get_db)) -> LemmaModel:
	return lemmi_crud.update_lemma(db=db, lemma_id=lemma_id, lemma=lemma)


@router.post("/delete/{id}")
async def delete_lemma(*, id: int, db: Session = Depends(get_db)) -> LemmaModel:
	return lemmi_crud.delete_lemma(db=db, lemma_id=id)