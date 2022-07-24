from fastapi import APIRouter, Depends, status
from pydantic import constr
from sqlalchemy.orm import Session

from dependency__db import get_db
from core_enums import FieldEnum, PageDirEnum, OrderEnum

import crud__lemmi as lemmi_crud
from models__lemmi import LemmaModel, LemmaFullTextSearchModel
from schemas__lemmi import LemmaSchema, LemmaListSchema

router = APIRouter(prefix="/lemmi")


@router.get("/list", response_model=LemmaListSchema)
async def list_lemmi(
	filter_by: FieldEnum | None = None,
	filter_value: str | None = None,
	order_by: FieldEnum = FieldEnum.lemma,
	order_value: OrderEnum = OrderEnum.asc,
	page_dir: PageDirEnum = PageDirEnum.next,
	page_size: int = 5,
	offset: int | str | None = None,
	db: Session = Depends(get_db)
) -> LemmaListSchema:
	lemmi = lemmi_crud.list_lemmi(
		filter_by=filter_by,
		filter_value=filter_value,
		order_by=order_by,
		order_value=order_value,
		page_dir=page_dir,
		page_size=page_size+1,
		offset=offset,
		db=db,
	)
	data_to_return = dict(
		data=lemmi,
		metadata=dict(
			filter_by=filter_by,
			filter_value=filter_value,
			order_by=order_by,
			order_value=order_value,
			page_dir=page_dir,
			page_size=page_size,
			offset=offset if len(lemmi) == page_size+1 else None,
		)
	)
	return data_to_return


@router.get("/view/{lemma_id}")
async def view_lemma(lemma_id: int, db: Session = Depends(get_db)) -> LemmaModel:
	return lemmi_crud.view_lemma(lemma_id=lemma_id, db=db)


@router.get("/search/{lemma}")
async def search_lemma(lemma: constr(min_length=3), exact: bool = False, db: Session = Depends(get_db)) -> list[LemmaFullTextSearchModel]:
	return lemmi_crud.search_lemma(lemma=lemma, exact=exact, db=db)


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_lemma(*, lemma: LemmaSchema, db: Session = Depends(get_db)) -> LemmaModel:
	return lemmi_crud.insert_lemma(lemma=lemma, db=db)


@router.put("/update/{lemma_id}")
async def update_lemma(*, lemma_id: int, lemma: LemmaSchema, db: Session = Depends(get_db)) -> LemmaModel:
	return lemmi_crud.update_lemma(lemma_id=lemma_id, lemma=lemma, db=db)


@router.delete("/delete/{lemma_id}")
async def delete_lemma(*, lemma_id: int, db: Session = Depends(get_db)) -> LemmaModel:
	return lemmi_crud.delete_lemma(lemma_id=lemma_id, db=db)